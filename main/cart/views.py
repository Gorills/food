from decimal import Decimal
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, ShopSetup
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from orders.forms import OrderCreateForm
from setup.models import ThemeSettings
from accounts.models import UserProfile
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'sushi'


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():

       
        

        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'],
                 
                 )
    return redirect('home')



def cart_remove(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
    except:
        pass
    return redirect('home')


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

    context = {
        'form': OrderCreateForm(request.POST),
        'cart': cart,
        'coupon_apply_form': coupon_apply_form
    }
    return render(request, 'global/detail.html', context)







def active_balls(request):
    cart = Cart(request)
    request.session['active_balls'] = str(cart.get_max_balls())


    return redirect('home')



def add_combo(request):
    cart = Cart(request)
    if request.method == 'POST':

        combo = request.POST['combo']
        combo_id = request.POST['combo']
        products = request.POST['products'][:-1]
        quantity = request.POST['quantity']
        price = request.POST['price']

        combo = combo + ','+products
        
       
        cart.add_combo(combo, combo_id, products, quantity, price)
        

    
    return redirect('/')




def remove_combo(request):
    cart = Cart(request)
    if request.method == 'POST':

        combo = request.POST['combo']
        
        
       
        cart.remove_combo(combo)
        

    
    return redirect('/')



def plus_combo(request):
    cart = Cart(request)
    if request.method == 'POST':
        combo = request.POST['combo']
       
        cart.plus_combo(combo)
        

    
    return redirect('/')


def minus_combo(request):
    cart = Cart(request)
    if request.method == 'POST':
        combo = request.POST['combo']
       
        cart.minus_combo(combo)
        

    
    return redirect('/')


def add_options(request):
    cart = Cart(request)
    if request.method == 'POST':

        
        options_id = request.POST['options_id']
        options = request.POST['options']
        products = request.POST['products']
        quantity = request.POST['quantity']
        price = request.POST['price']

        
        
       
        cart.add_options(options_id, options, products, quantity, price)
        

    
    return redirect('/')

def remove_options(request):
    cart = Cart(request)
    if request.method == 'POST':

        id = request.POST['id']

        cart.remove_options(id)
        

    
    return redirect('/')

def plus_options(request):
    cart = Cart(request)
    if request.method == 'POST':
        id = request.POST['id']
       
        cart.plus_options(id)
        

    
    return redirect('/')


def minus_options(request):
    cart = Cart(request)
    if request.method == 'POST':
        id = request.POST['id']
       
        cart.minus_options(id)
        

    
    return redirect('/')




def check_first_delivery(request):
    cart = Cart(request)
    first_delivery_persent = ShopSetup.objects.get().first_delivery

    if request.method == 'POST':
        phone = request.POST['phone']

        try:
            userprofile = UserProfile.objects.get(phone=phone)

            request.session['first_delivery'] = 0
            cart.first_delivery = 0
            print(userprofile)
            
        except Exception as e:
            
            cart.first_delivery = first_delivery_persent
            request.session['first_delivery'] = first_delivery_persent
            

        return redirect('home')
    

def set_delivery_detail(request):

    if request.method == 'POST':
        cart = Cart(request)

        
        price = request.POST['price'] 
        free = request.POST['free'] 
        min_delivery = request.POST['min_delivery']
        delivery_address = request.POST['delivery_address']
        
        request.session['delivery_summ'] = price
        request.session['free_delivery'] = free
        request.session['min_delivery'] = min_delivery

        


        data = {
            'street': delivery_address
        }
        
        request.session['delivery_address'] = data


        cart.add_address(delivery_address)
        cart.add_delivery_summ(price, free)
        cart.add_min_delivery(min_delivery)

        
        
        return redirect('home')


def set_delivery(request, value): 
    request.session['delivery'] = value
    return redirect('home')





    

def set_phone(request):
    if request.method == 'POST':
        cart = Cart(request)
        
        phone = request.POST['phone']
        data = {
            'phone': phone
        }
        
        
        cart.add_phone(data)
        request.session['phone'] = data
        
        print(cart.return_phone())
        return redirect('home')