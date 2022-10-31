from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm

from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')



def cart_remove(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
    except:
        pass
    return redirect('cart:cart_detail')


def cart_minus(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.minus(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])


    url = request.META.get('HTTP_REFERER')
    return redirect(url)


def cart_plus(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.plus(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
                 
        url = request.META.get('HTTP_REFERER')
        
        return redirect(url)

def cart_detail(request):
    cart = Cart(request)
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                            initial={'quantity': item['quantity'],
                            'update': True})
    
    if cart.coupon:
        data = {
            'code': cart.coupon.code
        }                 
        coupon_apply_form = CouponApplyForm(data)
    else:
        coupon_apply_form = CouponApplyForm()
    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form})