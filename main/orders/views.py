from django.shortcuts import render, redirect
from accounts.models import UserProfile

from shop.models import Product, ProductOption
from .models import Order, OrderItem
from .forms import CallbackForm, OrderCreateForm
from cart.cart import Cart
from setup.models import ThemeSettings
from accounts.models import UserProfile
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


from .telegram import order_telegram, send_message


from pay.models import PaymentSet
try:
    pay_name = PaymentSet.objects.get().name
except:
    pay_name = 'none'


# print(pay_name)


if pay_name == 'yookassa':
    from pay.yookassa_pay import create_payment

if pay_name == 'paykeeper':
    from pay.paykeeper_pay import create_payment, get_status




def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        pay_method = request.POST['pay_method']
        phone = request.POST['phone']

        if form.is_valid():

            try:
                user_pr = UserProfile.objects.get(phone=phone)
            except:
                user_pr = UserProfile.objects.create(phone=phone)


            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            
          
            order.user_pr = user_pr
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

            
            if pay_method == 'Оплата картой на сайте':

                if pay_name == 'yookassa':
                    data = create_payment(order, cart, request)
                    payment_id = data['id']
                    confirmation_url = data['confirmation_url']

                    order.payment_id = payment_id
                    order.payment_dop_info = confirmation_url
                    order.save()
                    print(data['path'])
                    return redirect(confirmation_url)
                if pay_name == 'paykeeper':

                    data = create_payment(order, cart, request)
                    payment_id = data['id']
                    confirmation_url = data['confirmation_url']

                    order.payment_id = payment_id
                    order.payment_dop_info = confirmation_url
                    order.save()
                    
                    return redirect(confirmation_url)


            else:
                order_telegram(order)
                # очистка корзины
                cart.clear()
                return redirect('/?order=True')
    else:

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,

                'phone': user_profile.phone,
              
                
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



from yookassa import Payment
def order_confirm(request, pk):
    cart = Cart(request)
    
    try:
        order = Order.objects.get(id=pk, paid=False, pay_method='Оплата картой на сайте')
        payment = Payment.find_one(order.payment_id)
        status = payment.status
        status = payment.status

        if status == 'succeeded':
            order_telegram(order)
            cart.clear()
            request.session['delivery'] = 1
            order.paid = True
            order.save()

            return redirect('/?order=True')

        context = {
            'order': order,
            'status': status,
            
        }

        return render(request, 'orders/order/confirm.html', context)
    except:

        return redirect('home')



def order_error(request):


    return render(request, 'orders/order/error.html')




def order_success(request):
    cart = Cart(request)

    pay_id = request.GET['orderId']

    data = get_status(pay_id)

    if data['status'] == '0':
        order = data['order']

        order_telegram(order)
        cart.clear()
        request.session['delivery'] = 1
        order.paid = True
        
        order.save()

        return redirect('/?order=True')

    else:
        return redirect('orders:order_error')