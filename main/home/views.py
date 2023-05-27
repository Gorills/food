import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from accounts.models import LoyaltyCardSettings
from orders.models import Order
from shop.models import Category, Manufacturer, ShopSetup, Product
from setup.models import BaseSettings, Colors, EmailSettings
from .models import SliderSetup, Slider, Page
from blog.models import BlogSetup, Post
from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'sushi'

from django.views.generic import TemplateView, ListView

from pay.models import AlfaBank, PaymentSet, Yookassa


from pay.paykeeper_pay import get_status
from subdomains.utilites import get_protocol
# get_status()



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


    try:
        setup = BaseSettings.objects.get()
        shop_setup = ShopSetup.objects.get()
        blog_setup = BlogSetup.objects.get()
        email = EmailSettings.objects.get()
        theme = ThemeSettings.objects.get()
        colors = Colors.objects.get()
    except:
        setup = BaseSettings()
        shop_setup = ShopSetup()
        blog_setup = BlogSetup()
        email = EmailSettings()
        theme = ThemeSettings()
        colors = Colors()
        colors.save()
        theme.save()
        email.save()
        setup.save()
        shop_setup.save()
        blog_setup.save()


    order_get = request.GET.getlist('order')
    home_cats = Category.objects.filter(home=True)[:7]

    try:
        slider_setup = SliderSetup.objects.get()
    except:
        slider_setup = SliderSetup.objects.create()

    try:
        loyal = LoyaltyCardSettings.objects.get()
    except:
        loyal = LoyaltyCardSettings.objects.create()

    try:
        shop_setup = ShopSetup.objects.get()
    except:
        shop_setup = ShopSetup.objects.create()

    sliders = Slider.objects.filter(day__in=[7, current_day])

    new_products = Product.objects.filter(new=True, status=True).exclude(stock=0).order_by('-id')[:8]
    sale_products = Product.objects.filter(status=True).exclude(old_price=None).exclude(stock=0)[:8]
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


    context = {
        'current_day': current_day,
        'order': order_object,
        'home_cats': home_cats,
        'slider_setup': slider_setup,
        'sliders': sliders,
        'shop_setup': shop_setup,
        'new_products': new_products,
        'sale_products': sale_products,
        'news': news,
        'hit_products': hit_products,
        'order_get': order_get
    }
    
    return render(request, 'home/home.html', context)



def page_detail(request, slug):
    page = get_object_or_404(Page, type=slug, status=True)
    context = {
        'page': page
    }
    return render(request, 'home/page_detail.html', context)


from django.db.models import Q
class SearchResultsView(ListView):
    model = Product
    template_name = 'global/search_detail.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query)
        )