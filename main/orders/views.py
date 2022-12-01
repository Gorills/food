from django.shortcuts import render, redirect
from accounts.models import UserProfile

from shop.models import Product, ProductOption
from .models import OrderItem
from .forms import CallbackForm, OrderCreateForm
from cart.cart import Cart
from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


from .telegram import order_telegram, send_message


from pay.models import Payment
pay_name = Payment.objects.get().name

if pay_name == 'yookassa':
    
    from pay.yookassa_pay import create_payment

    # print(create_payment())




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
            order.delivery_price = cart.get_delivery()
            order.save()


            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                    )
                
                pr = Product.objects.get(id=item['product'].id)

                # Добавляем продажу для учета хитов продаж
                sales_old = pr.sales
                sales_new = int(sales_old)+int(item['quantity'])
                
                pr.sales = sales_new

                # Отнимаем количество, если указано в настройках
                if pr.subtract == True:
                    pr.stock = pr.stock - item['quantity']
                    if pr.stock < 0:
                        pr.stock = 0

                    

                pr.save()

            if pay_name == 'yookassa':
                return redirect(create_payment(order, cart))
            else:
                order_telegram(order)
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





def order_callback(request):
    if request.method == 'POST':

        form = CallbackForm(request.POST)
        name = request.POST['name']
        tel = request.POST['phone']
        messages = request.POST['messages']

        message = "Заказ обратного звонка:" + "\n" + "*ИМЯ*: " +str(name) + "\n" + "*ТЕЛЕФОН*: " + str(tel) + "\n" + "*СООБЩЕНИЕ*: " +str(messages)
        
        if form.is_valid():
            send_message(message)

            
            return redirect('orders:thank')

def thank(request):



    return render(request, 'orders/order/created.html')