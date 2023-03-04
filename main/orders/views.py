
from django.shortcuts import render, redirect
from accounts.models import LoyaltyCard, LoyaltyCardSettings, UserProfile
import requests
from shop.models import Product, ProductOption
from .models import Order, OrderItem
from .forms import CallbackForm, OrderCreateForm
from cart.cart import Cart
from setup.models import ThemeSettings
from accounts.models import UserProfile
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


from .telegram import order_telegram, send_message
from sms.views import send_sms

from pay.models import PaymentSet
try:
    pay_name = PaymentSet.objects.get().name
except:
    pay_name = 'none'


# print(pay_name)


if pay_name == 'yookassa':
    from pay.yookassa_pay import create_payment

if pay_name == 'alfabank':
    from pay.alfabank_pay import create_payment, get_status

if pay_name == 'paykeeper':
    from pay.paykeeper_pay import create_payment, get_status

if pay_name == 'tinkoff':
    from pay.tinkoff_pay import create_payment




def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        pay_method = request.POST['pay_method']
        phone = request.POST['phone']

        try:
            domofon = request.POST['domofon']
            if domofon == '':
                domofon = request.POST['flat']
        except:
            domofon = request.POST['flat']

        if form.is_valid():

            try:
                user_pr = UserProfile.objects.get(phone=phone)
            except:
                user_pr = UserProfile.objects.create(phone=phone)


            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            
            if cart.active_balls:
                order.balls = cart.active_balls
          
            order.user_pr = user_pr
            order.summ = cart.get_total_price_after_discount()
            order.delivery_price = cart.get_delivery()

            # Бонусы сохраняем в заказ
            if cart.active_balls > 0:
                order.bonuses_pay = cart.active_balls

            
            order.flat = str(order.flat) + ' (домофон: ' + str(domofon) + ')'

            order.save()


            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    free=item['free'],
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
                    
                if pay_name == 'alfabank':

                    data = create_payment(order, cart, request)
                    payment_id = data['id']
                    confirmation_url = data['confirmation_url']

                    order.payment_id = payment_id
                    order.payment_dop_info = confirmation_url
                    order.save()
                    
                    return redirect(confirmation_url)

                if pay_name == 'paykeeper':

                    data = create_payment(order, cart, request)
                    payment_id = data['id']
                    confirmation_url = data['confirmation_url']
                   
                    # session_url = 'http://' + request.META['HTTP_HOST']+'/orders/paykeeper/session/' + payment_id + '/'
                    # requests.post(session_url)

                    order.payment_id = payment_id
                    order.payment_dop_info = confirmation_url
                    order.save()
                    
                    print(confirmation_url)
                    return redirect('/orders/paykeeper/session/' + payment_id + '/')
                
                if pay_name == 'tinkoff':
                    data = create_payment(order, request)

                    
                    order.payment_dop_info = data
                    order.save()

                    return redirect(data)



            else:
                order_telegram(order)
                text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
                send_sms(text, phone)
                # очистка корзины
                
                
                if LoyaltyCardSettings.objects.get().active == True:
                    user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])

                    try:
                       
                        loyalty_card = LoyaltyCard.objects.get(user=user_profile)
                    
                    except:
                        loyalty_card = LoyaltyCard.objects.create(
                            user=user_profile,
                            summ=Decimal('0.00')
                            )

                    try:
                        if order.bonuses_pay > 0:
                            loyalty_card.balls = loyalty_card.balls - order.bonuses_pay

                    except:
                        pass
                    
                    loyalty_card.save()

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
        

        if status == 'succeeded':
            order_telegram(order)
            text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
            send_sms(text, order.phone)

            if LoyaltyCardSettings.objects.get().active == True:
                user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
                try:
                    loyalty_card = LoyaltyCard.objects.get(user=user_profile)
                except:
                    loyalty_card = LoyaltyCard.objects.create(
                        user=user_profile,
                        summ=Decimal('0.00')
                        )

                try:
                    if order.bonuses_pay > 0:
                        loyalty_card.balls = loyalty_card.balls - order.bonuses_pay

                except:
                    pass
                
                loyalty_card.save()


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

# Проверка событий Юкассы не работает
import logging
logger = logging.getLogger(__name__)
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import WebhookNotification
@csrf_exempt
def order_webhook(request):
    if request.method == 'POST':
        event_json = json.loads(request.body)
            
        try:
            notification_object = WebhookNotification(event_json)
        except Exception as e:
            print(e)
          
        # Получите объекта платежа
        payment = notification_object.object
        logger.info(payment.id)
        pay_id = payment.id
        try:
            order = Order.objects.get(payment_id=pay_id, paid=False, pay_method='Оплата картой на сайте')
            payment = Payment.find_one(pay_id)
            status = payment.status
            if status == 'succeeded':
                
                order_telegram(order)
                text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
                send_sms(text, order.phone)
                order.paid = True
                order.save()

                if LoyaltyCardSettings.objects.get().active == True:
                    user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
                    try:
                        loyalty_card = LoyaltyCard.objects.get(user=user_profile)
                    except:
                        loyalty_card = LoyaltyCard.objects.create(
                            user=user_profile,
                            summ=Decimal('0.00')
                            )

                    try:
                        if order.bonuses_pay > 0:
                            loyalty_card.balls = loyalty_card.balls - order.bonuses_pay

                    except:
                        pass
                    
                    loyalty_card.save()


                return HttpResponse(status=200)
        except Exception as e:
            logger.info(e)
            return HttpResponse(status=200)



def order_error(request):
    return render(request, 'orders/order/error.html')


def order_success(request):
    cart = Cart(request)

    pay_id = request.GET['orderId']

    data = get_status(pay_id)

    if data['status'] == '0':
        order = data['order']

        order_telegram(order)
        
        text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
        send_sms(text, order.phone)

        if LoyaltyCardSettings.objects.get().active == True:
            user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
            try:
                loyalty_card = LoyaltyCard.objects.get(user=user_profile)
            except:
                loyalty_card = LoyaltyCard.objects.create(
                    user=user_profile,
                    summ=Decimal('0.00')
                    )

            try:
                if order.bonuses_pay > 0:
                    loyalty_card.balls = loyalty_card.balls - order.bonuses_pay

            except:
                pass
            
            loyalty_card.save()



        cart.clear()
        request.session['delivery'] = 1
        order.paid = True
        
        order.save()

        return redirect('/?order=True')

    else:
        return redirect('orders:order_error')



def paykeeper_error(request):
    return render(request, 'orders/order/error.html')


@csrf_exempt 
def paykeeper_session(request, pk):
    
    request.session['myorder_id'] = str(pk)
    request.session.modified = True
    
    order = Order.objects.get(payment_id=request.session['myorder_id']).payment_dop_info

    print(order)

    return redirect(order) 

    
    


def paykeeper_success(request):
    cart = Cart(request)

    pay_id = request.session['myorder_id']
    
    print(pay_id)

    data = get_status(pay_id)

    if data['status'] == 'paid':
        order = data['order']

        order_telegram(order)
        text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
        send_sms(text, order.phone)

        if LoyaltyCardSettings.objects.get().active == True:
            user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
            try:
                loyalty_card = LoyaltyCard.objects.get(user=user_profile)
            except:
                loyalty_card = LoyaltyCard.objects.create(
                    user=user_profile,
                    summ=Decimal('0.00')
                    )

            try:
                if order.bonuses_pay > 0:
                    loyalty_card.balls = loyalty_card.balls - order.bonuses_pay

            except:
                pass
            
            loyalty_card.save()



        cart.clear()
        request.session['delivery'] = 1
        request.session['myorder_id'] = 0

        order.paid = True
        
        order.save()

        return redirect('/?order=True')

    else:
        return redirect('orders:paykeeper_error')
    




def tinkoff_success(request, pk):
    cart = Cart(request)
    cart.clear()

    order = Order.objects.get(id=pk)
    order.paid = True
    order.save()
    order_telegram(order)
    text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
    send_sms(text, order.phone)
    
    return redirect('/?order=True')