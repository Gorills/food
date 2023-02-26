import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from shop.models import Manufacturer, ShopSetup, Product
from setup.models import BaseSettings
from .models import SliderSetup, Slider, Page
from blog.models import Post
from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'

from django.views.generic import TemplateView, ListView

from pay.models import AlfaBank, PaymentSet, Yookassa


from pay.paykeeper_pay import get_status
# get_status()



@require_GET
def robots_txt(request):
    try:
        setup = BaseSettings.objects.get()
        sitemap_txt = 'Sitemap: https://' + str(request.META['HTTP_HOST'])+'/sitemap.xml'
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

from decimal import Decimal

def home(request):

    if request.method == 'POST':
        get_cookie = request.POST['get_cookie']
        if get_cookie == 'ZcMWy~DhAiTo0@~':
            request.session['get_cookie'] = 'True'

    # payment = PaymentSet.objects.get()
    # payment.delete()
    # yookassa = Yookassa.objects.get()
    # yookassa.delete()
    # AlfaBank = AlfaBank.objects.get()
    # AlfaBank.delete()
    # cart = Cart(request)
    # cart.clear()
    order_get = request.GET.getlist('order')
    
    slider_setup = SliderSetup.objects.get()
    shop_setup = ShopSetup.objects.get()
    sliders = Slider.objects.all()
    new_products = Product.objects.filter(new=True).order_by('-id')[:8]
    sale_products = Product.objects.all().exclude(old_price=None)[:8]
    hit_products = Product.objects.all().order_by('-sales').exclude(sales=0)[:8]
    news = Post.objects.all().order_by('-id').exclude(draft=True)[:4]


    context = {
       
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
    page = get_object_or_404(Page, type=slug)
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