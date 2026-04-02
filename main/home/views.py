import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET
from sorl.thumbnail import get_thumbnail
from django.http import HttpResponse
from accounts.models import LoyaltyCardSettings
from orders.models import Order
from shop.models import Category, CategorySetup, Manufacturer, PickupAreas, ProductSale, ShopSetup, Product
from setup.models import BaseSettings, Colors, EmailSettings
from .models import SliderSetup, Slider, Page, PlaceImages, Reviews
from blog.models import BlogSetup, Post
from setup.models import ThemeSettings
from django.http import JsonResponse
import json
try:
    theme_address = ThemeSettings.objects.get().name
except Exception:
    theme_address = 'fast_theme'

from django.views.generic import TemplateView, ListView

from pay.models import AlfaBank, PaymentSet, Yookassa

from integrations.views import *
from pay.paykeeper_pay import get_status
from subdomains.utilites import get_protocol
from delivery.yandex_eda import *



# get_status()

def decimal_encoder(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def manifest_json(request):
    try:
        data_from_db = BaseSettings.objects.get()
        theme_setup = Colors.objects.get()
    except Exception:
        manifest_data = {
            "name": "Site",
            "short_name": "Site",
            "start_url": ".",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#333333",
            "icons": []
        }
        response_data = json.dumps(manifest_data, ensure_ascii=False, default=decimal_encoder)
        return HttpResponse(response_data, content_type='application/json')

    name = str(data_from_db.name).strip() if getattr(data_from_db, 'name', None) else "Site"
    theme_color = getattr(theme_setup, 'primary', None) or '#333333'
    theme_color = str(theme_color).strip() if theme_color else '#333333'
    manifest_data = {
        "name": name or "Site",
        "short_name": name or "Site",
        "start_url": ".",
        "display": "standalone",
        "background_color": str(getattr(theme_setup, 'body_bg', '#ffffff') or '#ffffff'),
        "theme_color": theme_color,
        "icons": []
    }

    if data_from_db.icon_png:
        try:
            for size in ['48x48', '72x72', '96x96', '144x144', '192x192', '512x512']:
                thumb = get_thumbnail(data_from_db.icon_png, size, format="PNG", crop='center', quality=100)
                if thumb:
                    manifest_data["icons"].append({
                        "src": '/main/media/' + str(thumb),
                        "sizes": size,
                        "type": "image/png"
                    })
        except Exception:
            pass

    response_data = json.dumps(manifest_data, ensure_ascii=False, default=decimal_encoder)
    return HttpResponse(response_data, content_type='application/json')

@require_GET
def robots_txt(request):
    try:
        setup = BaseSettings.objects.get()
        sitemap_txt = f'Sitemap: {get_protocol(request)}://{request.META["HTTP_HOST"]}/sitemap.xml'
        if setup.active == True:
            lines = [
                "User-Agent: *",
                "Disallow: /admin/",
                "Disallow: /orders/",
                "Disallow: /cart/",
                "Disallow: /coupons/",
                "Disallow: /accounts/",
                "Disallow: /login/",
                "Disallow: /logout/",
                "Disallow: *utm=",
                "Disallow: /order/",
                "Disallow: /search/",
                "Disallow: /bonus/",
                "Disallow: *?sort=",
                "Disallow: *?page=",
                "Disallow: *?limit=",
                "Disallow: *?order=",
                "Disallow: /catalog/set_like/",
                "Disallow: /catalog/products/product_options/",

                "User-Agent: Yandex",
                "Disallow: /admin/",
                "Disallow: /orders/",
                "Disallow: /cart/",
                "Disallow: /coupons/",
                "Disallow: /accounts/",
                "Disallow: /login/",
                "Disallow: /logout/",
                "Disallow: *utm=",
                "Disallow: /order/",
                "Disallow: /search/",
                "Disallow: /bonus/",
                "Disallow: *?sort=",
                "Disallow: *?page=",
                "Disallow: *?limit=",
                "Disallow: *?order=",
                "Disallow: /catalog/set_like/",
                "Disallow: /catalog/products/product_options/",
                "Clean-Param: utm_source&utm_medium&utm_campaign",

                sitemap_txt
            ]
        else:
            lines = [
                "User-Agent: *",
                "Disallow: /",
                
            ]

    except:
        lines = [
            "User-Agent: *",
            "Disallow: /",
            
        ]
        
    return HttpResponse("\n".join(lines), content_type="text/plain")




def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)




def home_login(request):

    try:
        user_id = request.session['user_profile_id']
    except:
        user_id = None

    if user_id:
        return redirect('account:account_profile')
    context = {
    }
    return render(request, 'global/login.html', context)


def home_logout(request):

    del request.session['user_profile_id']
    return redirect('home_login')
    


from cart.cart import Cart
from datetime import datetime

from decimal import Decimal
from subdomains.utilites import get_subdomain


def home(request):

    current_day = datetime.today().weekday()
    if request.method == 'POST':
        get_cookie = request.POST['get_cookie']
        if get_cookie == 'ZcMWy~DhAiTo0@~':
            request.session['get_cookie'] = 'True'

    # print(current_day)

    # payment = PaymentSet.objects.get()
    # payment.delete()
    # yookassa = Yookassa.objects.get()
    # yookassa.delete()
    # AlfaBank = AlfaBank.objects.get()
    # AlfaBank.delete()
    # cart = Cart(request)
    # cart.clear()
    # cart.options_clear()
    # cart.combo_clear()





    order_get = request.GET.getlist('order')

    
    
    home_cats_setup = CategorySetup.objects.filter(home=True).order_by('sort_order')

    # Собираем список ID категорий
    category_ids = [cat.get_category().id for cat in home_cats_setup if cat.get_category()]

    if home_cats_setup.count() > 0:
        # Преобразуем список ID в QuerySet
        home_cats = Category.objects.filter(id__in=category_ids).order_by('sort_order')
    else:
        home_cats = Category.objects.filter(home=True, show_in_site=True, status=True).order_by('sort_order')



    sliders = Slider.objects.filter(day__in=[7, current_day], show=True).order_by('order')

    new_products = Product.objects.filter(new=True, status=True).exclude(stock=0).order_by('-id')[:8]

    

    # Получить все товары
    all_products = Product.objects.filter(status=True).exclude(stock=0)

    # Фильтровать товары с ненулевой скидкой
    sale_products_list = []
    for product in all_products:
        if product.get_sale():
            if product.get_sale() > 0:
                sale_products_list.append(product.id)

    sale_products = Product.objects.filter(id__in=sale_products_list)[:8]


    hit_products = Product.objects.filter(bestseller=True, status=True).exclude(stock=0)[:8]
    if hit_products.count() == 0:

        hit_products = Product.objects.all().order_by('-sales').exclude(sales=0).exclude(related=True).exclude(stock=0)[:8]

    news = Post.objects.all().order_by('-id').exclude(draft=True)[:4]


    try:
        order_id = request.GET.get('id')
        order = Order.objects.get(id=order_id)

        products = []
        for item in order.items.all():
            if item.product:
                if not item.product.related:
                    item_one = {
                        "id": item.product.id,
                        "name": item.product.name,
                        "price": str(item.price),
                    
                        "category": item.product.parent.name,
                        
                        "quantity": item.quantity
                    }
                    products.append(item_one)
            elif item.combo:
                
                item_one = {
                    "id": item.combo.id,
                    "name": item.combo.name,
                    "price": str(item.price),
                
                    "category": 'Комбо',
                    
                    "quantity": item.quantity
                }
                products.append(item_one)


        order_object = {
            "ecommerce": {
                "currencyCode": "RUB",
                "purchase": {
                    "actionField": {
                        "id" : f"{order.id}"
                    },
                    "products": products
                }
            }
        }
    except Exception as e:
        # print(e)
        order_object = {}
    

    # print(order_object)
    try:
        slider_setup = SliderSetup.objects.get()
    except:
        slider_setup = SliderSetup()
        slider_setup.save()

    context = {
        'current_day': current_day,
        'order': order_object,
        'home_cats': home_cats,
        'slider_setup': slider_setup,
        'sliders': sliders,
        
        'new_products': new_products,
        'sale_products': sale_products,
        'news': news,
        'hit_products': hit_products,
        'order_get': order_get,
        'get_domain': get_subdomain(request),
        'reviews': Reviews.objects.filter(view_home=True),
    }
    
    return render(request, 'home/home.html', context)



def page_detail(request, slug):
    page = get_object_or_404(Page, type=slug, status=True)
    pickup_areas = PickupAreas.objects.all()
    context = {
        'page': page,
        'pickup_areas': pickup_areas,
        'images': PlaceImages.objects.all(),
    }
    return render(request, 'home/page_detail.html', context)


from django.db.models import Q
class SearchResultsView(ListView):
    model = Product
    template_name = 'global/search_detail.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query), status=True
        )
    


from urllib.parse import unquote
import idna


def _privacy_page_context(request):
    """
    Для IDNA нужно имя хоста без порта: HTTP_HOST вида 127.0.0.1:8000 ломает
    idna.decode() (InvalidCodepoint на ':'). URL сайта собираем с полным host:port.
    """
    host_header = (request.META.get('HTTP_HOST') or '').strip()
    host_only = host_header
    if host_header.startswith('['):
        end = host_header.find(']')
        if end != -1:
            host_only = host_header[1:end]
    elif ':' in host_header and host_header.count(':') == 1:
        host_only = host_header.split(':', 1)[0]
    try:
        decoded_domain = idna.decode(host_only)
    except Exception:
        decoded_domain = host_only
    site = f'{get_protocol(request)}://{host_header}'
    privacy_email = f'privacy@{decoded_domain}'
    return {'site': site, 'privacy_email': privacy_email}


def privacy(request):
    return render(request, 'home/privacy.html', _privacy_page_context(request))



def info(request):

    
    return render(request, 'home/info.html')


def user_agreement(request):
    return render(request, 'home/user_agreement.html', _privacy_page_context(request))


def consent(request):
    return render(request, 'home/consent.html', _privacy_page_context(request))