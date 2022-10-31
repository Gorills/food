from django.shortcuts import render, redirect
from accounts.models import UserProfile

from shop.models import Product, ProductOption
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            
            if request.user.is_authenticated:
                user = request.user
                order.user = user

            else:
                order.user = None

            order.summ = cart.get_total_price_after_discount()
            order.save()


            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    option=item['option'],
                    price=item['price'],
                    quantity=item['quantity']
                    )
                
                pr = ProductOption.objects.get(id=item['option'].id)

                # Добавляем продажу для учета хитов продаж
                sales_old = pr.parent.sales
                sales_new = int(sales_old)+int(item['quantity'])
                prod = pr.parent
                prod.sales = sales_new

                # Отнимаем количество, если указано в настройках
                if prod.subtract == True:
                    prod.stock = prod.stock - item['quantity']
                    if prod.stock < 0:
                        prod.stock = 0

                    

                prod.save()

                


            # очистка корзины
            cart.clear()
            return redirect('orders:thank')
    else:

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,

                'phone': user_profile.telephone,
                'apartment': user_profile.apartment,
                'address': user_profile.address,
                'postal_code': user_profile.postal_code,
                'city': user_profile.city,
            }
            form = OrderCreateForm(data)

        except Exception as e:
            print(e)
            form = OrderCreateForm()
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


def thank(request):



    return render(request, 'orders/order/created.html')