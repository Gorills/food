
from django.shortcuts import render, redirect
from accounts.models import LoyaltyCard, LoyaltyCardSettings, UserProfile
import requests
from integrations.iiko import create_iiko_order
from subdomains.utilites import get_subdomain
from shop.models import ComboItem, Product, ProductOption, ShopSetup
from .models import Order, OrderItem
from .forms import CallbackForm, OrderCreateForm
from cart.cart import Cart
from setup.models import ThemeSettings, BaseSettings
from accounts.models import UserProfile
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal



try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'sushi'




def sms_text(order_id, summ):

    try:
        text_standart = BaseSettings.objects.get().sms_text
    except:
        text_standart = f'Ваш заказ принят. Ему присвоен № {order_id}.'
    else:
        text_standart = f'Ваш заказ принят. Ему присвоен № {order_id}.'

    
    text = text_standart.replace('{order}', str(order_id)).replace('{summ}', str(summ))
    
    
    return text



try:
    telegram_bot = BaseSettings.objects.get().telegram_bot
    telegram_group = BaseSettings.objects.get().telegram_group
except Exception as e:
    
    telegram_bot = ''
    telegram_group = ''


from .telegram import order_telegram, send_message
from sms.views import send_sms
from .send_email import send_order_email
from pay.alfabank_pay import start_background_task

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
    subdomain = get_subdomain(request)

    if subdomain and subdomain.telegram_group:
        telegram_group = subdomain.telegram_group
    else:
        telegram_group = BaseSettings.objects.get().telegram_group
    
    if cart:
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)

            pay_method = request.POST['pay_method']
            phone = request.POST['phone']
            name = request.POST['name']
            try:
                pay_change = request.POST['pay_change']
                order.pay_change = pay_change
            except:
                pay_change = None
            

            try:
                domofon = request.POST['door_code']
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
                
                order.delivery_price = Decimal(cart.get_delivery())
                try:
                    order.sale_percent = cart.get_discount_on_pickup_persent() + cart.first_delivery
                except:
                    order.sale_percent = 0
                

                # Бонусы сохраняем в заказ
                if cart.active_balls > 0:
                    order.bonuses_pay = cart.active_balls
                    order.percent_pay = cart.percent_pay

                
                if order.flat:
                    order.flat = str(order.flat)
                
                

                order.door_code = domofon
                order.name = name
                order.save()
                
                

                for item in cart:
                    
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        free=item['free'],
                        quantity=item['quantity'],
                        weight=item['product'].weight
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

                combos = cart.get_combos()

                for combo in combos:

                    combo_items = ''
                    for pr in combo['products']:
                        combo_items = combo_items + pr.product.name + ', '

                    
                    combo_items = combo_items[:-1]

                    OrderItem.objects.create(
                        order=order,
                        combo=combo['combo'],
                        price=combo['price'],
                        combo_items = combo_items,
                        quantity=combo['quantity']
                        )
                    
                options = cart.get_options()
                for option in options:

                    text_opt = option['options']
                    options_str_list = []
                    for key, value in text_opt.items():
                        options_str = f"{key.name}: "
                        if key.name == 'Размер':
                            options_str += f"{value[0].option_value}см"
                        else:
                            options_str += ", ".join([opt.option_value for opt in value])
                        options_str_list.append(options_str)
                    options_str = "; ".join(options_str_list)

                    OrderItem.objects.create(
                        order=order,
                        product=option['products'],
                        price=option['price'],
                        options=options_str,
                        quantity=option['quantity']
                    )


                constructors = cart.get_constructors()
                for constructor in constructors:
                    
                    constructor_items = ''
                    for con in constructor['items']:
                        constructor_items = constructor_items + con.name + ', '

                    
                    constructor_items = constructor_items[:-1]

                    OrderItem.objects.create(
                        order=order,
                        constructor=constructor['constructor'],
                        price=constructor['price'],
                        constructor_items=constructor_items,
                        quantity=constructor['quantity']
                    )
                    

                if pay_method == 'Оплата картой на сайте':

                    # отправлять заказ в телеграм бот, даже если не прошла оплата
                    info_to_order_anyway = ShopSetup.objects.get().info_to_order_anyway
                    
                    if info_to_order_anyway:
                        order_telegram(telegram_bot, telegram_group, order, request)


                    if pay_name == 'yookassa':
                        data = create_payment(order, cart, request)
                        payment_id = data['id']
                        confirmation_url = data['confirmation_url']

                        order.payment_id = payment_id
                        order.payment_dop_info = confirmation_url
                        order.save()
                        # print(data['path'])
                        return redirect(confirmation_url)
                        
                    if pay_name == 'alfabank':

                        data = create_payment(order, cart, request)
                        payment_id = data['id']
                        confirmation_url = data['confirmation_url']

                        order.payment_id = payment_id
                        order.payment_dop_info = confirmation_url
                        order.save()

                        start_background_task(order.payment_id)
                        
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

                        print(data['hashed_value'])
                        order.payment_dop_info = data['hashed_value']
                        order.payment_id = data['payment_id']
                        order.save()

                        return redirect(data['confirmation_url'])



                else:
                    order_telegram(telegram_bot, telegram_group, order, request)

                    try:
                        send_order_email(order)
                    except Exception as e:
                        pass
                        
                    
                    send_sms(sms_text(order.id, order.summ), phone)
                    
                    # очистка корзины
                    
                    
                    if LoyaltyCardSettings.objects.get().active == True and BaseSettings.objects.get().sms == True:
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

                    cart.options_clear()
                    cart.combo_clear()
                    cart.constructor_clear()
                    cart.clear()
                    request.session['first_delivery'] = 0

                    return redirect(f'/?order=True&id={order.id}')
                

            else:
                pass
                # print(form)
        else:
            return redirect('home')

        #     try:
        #         user_profile = UserProfile.objects.get(user=request.user)
        #         data = {
        #             'first_name': request.user.first_name,
        #             'last_name': request.user.last_name,
        #             'email': request.user.email,

        #             'phone': user_profile.phone,
                
                    
        #         }
        #         form = OrderCreateForm(data)

        #     except Exception as e:
        #         print(e)
        #         form = OrderCreateForm()
        # return render(request, 'orders/order/create.html',
        #               {'cart': cart, 'form': form})





def order_callback(request):
    if request.method == 'POST':

        form = CallbackForm(request.POST)
        name = request.POST['name']
        tel = request.POST['phone']
        messages = request.POST['messages']

        message = "Заказ обратного звонка:" + "\n" + "*ИМЯ*: " +str(name) + "\n" + "*ТЕЛЕФОН*: " + str(tel) + "\n" + "*СООБЩЕНИЕ*: " +str(messages)
        
        if form.is_valid():
            send_message(telegram_bot, telegram_group, message)

            
            return redirect('orders:thank')

def thank(request):



    return render(request, 'orders/order/created.html')



from yookassa import Payment
def order_confirm(request, pk):
    cart = Cart(request)
    subdomain = get_subdomain(request)
    try:
        telegram_bot = subdomain.telegram_bot
    except:
        telegram_bot = BaseSettings.objects.get().telegram_bot
    try:
        telegram_group = subdomain.telegram_group
    except:
        telegram_group = BaseSettings.objects.get().telegram_group

    try:
        order = Order.objects.get(id=pk)
        payment = Payment.find_one(order.payment_id)
        status = payment.status
        

        if status == 'succeeded':
            

            if LoyaltyCardSettings.objects.get().active == True and BaseSettings.objects.get().sms == True: 
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


            cart.combo_clear()
            cart.clear()
            cart.constructor_clear()
            request.session['delivery'] = 1

            if order.paid == False:

                order.paid = True
                order.save()

                order_telegram(telegram_bot, telegram_group, order, request)
                
                # send_sms(sms_text(order.id, order.summ), order.phone)

            return redirect(f'/?order=True')
        

        

        context = {
            'order': order,
            'status': status,
            
        }

        return render(request, 'orders/order/confirm.html', context)
    except Exception as e:

        order_telegram(telegram_bot, telegram_group, e)

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
    subdomain = get_subdomain(request)
    try:
        telegram_bot = subdomain.telegram_bot
    except:
        telegram_bot = BaseSettings.objects.get().telegram_bot
    try:
        telegram_group = subdomain.telegram_group
    except:
        telegram_group = BaseSettings.objects.get().telegram_group

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
            order = Order.objects.get(payment_id=pay_id, paid=False)
            payment = Payment.find_one(pay_id)
            status = payment.status
            if status == 'succeeded':
                
                
                order.paid = True
                order.save()

                order_telegram(telegram_bot, telegram_group, order, request)
                
                send_sms(sms_text(order.id, order.summ), order.phone)
                # create_iiko_order(order)

                try:

                    if LoyaltyCardSettings.objects.get().active == True:
                        user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
                        try:
                            loyalty_card = LoyaltyCard.objects.get(user=user_profile)
                            loyalty_card.summ += order.summ
                            loyalty_card.save()
                        except:
                            loyalty_card = LoyaltyCard.objects.create(
                                user=user_profile,
                                summ=Decimal('0.00')
                                )
                            loyalty_card.summ += order.summ
                            loyalty_card.save()
                        try:
                            if order.bonuses_pay > 0:
                                loyalty_card.balls = loyalty_card.balls - order.bonuses_pay

                        except:
                            pass
                        
                        loyalty_card.save()
                except:
                    pass


                return HttpResponse(status=200)
        except Exception as e:
            order_telegram(request, telegram_bot, telegram_group, e)
            logger.info(e)
            return HttpResponse(status=200)



def order_error(request):
    return render(request, 'orders/order/error.html')


# Альфабанк

def alpha_check(request, pk):

    order = Order.objects.get(id=pk)
    pay_id = order.payment_id
    data = get_status(pay_id)
     
    if data['status'] == 2:
        order = data['order']

        
        print(data['status'])

       
        order.paid = True
        
        order.save()

        order_telegram(telegram_bot, telegram_group, order, request)

    return redirect('admin_order')

  



def order_success(request):


    cart = Cart(request)

    pay_id = request.GET['orderId']

    data = get_status(pay_id)

    order = data['order']
    
    return redirect(f'/?order=True&id={order.id}')



from django.http import JsonResponse

wo_elegram_bot = '5953442472:AAHsgzGdcVrnuJnb0FnDWJ4nrPdDT59YNOE'
wo_telegram_group = '-1001850576262'

@csrf_exempt
def alfabank_callback(request):
    """
    Обработка callback-уведомлений от банка
    """
    # if request.method != 'GET':
    #     error_message = 'Invalid request method'
    #     send_message(wo_elegram_bot, wo_telegram_group, error_message)
    #     return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Получение параметров из запроса
    md_order = request.GET.get('mdOrder')
    order_number = request.GET.get('orderNumber')
    operation = request.GET.get('operation')
    status = request.GET.get('status')
    callback_creation_date = request.GET.get('callbackCreationDate')

    # Проверка обязательных параметров
    if not all([md_order, order_number, operation, status, callback_creation_date]):
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    error_message = f'Error: {order_number} {operation} {status}'
    send_message(wo_elegram_bot, wo_telegram_group, error_message)

    try:
        order = Order.objects.get(payment_id=md_order)
        order.paid = True
        order.save()
        
        order_telegram(telegram_bot, telegram_group, order)

    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    # # Возвращаем успешный ответ
    return JsonResponse({'success': True, 'message': 'Callback processed successfully'})


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
    subdomain = get_subdomain(request)
    try:
        telegram_bot = subdomain.telegram_bot
    except:
        telegram_bot = BaseSettings.objects.get().telegram_bot
    try:
        telegram_group = subdomain.telegram_group
    except:
        telegram_group = BaseSettings.objects.get().telegram_group
    
    

    data = get_status(pay_id)

    if data['status'] == 'paid':
        order = data['order']

        

        if LoyaltyCardSettings.objects.get().active == True:
            user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
            try:
                loyalty_card = LoyaltyCard.objects.get(user=user_profile)
                loyalty_card.summ += order.summ
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


        cart.combo_clear()
        cart.clear()
        cart.constructor_clear()
        request.session['delivery'] = 1
        request.session['myorder_id'] = 0

        order.paid = True
        
        order.save()

        order_telegram(telegram_bot, telegram_group, order, request)
        
        send_sms(sms_text(order.id, order.summ), order.phone)

        return redirect(f'/?order=True&id={order.id}')

    else:
        return redirect('orders:paykeeper_error')
    




def tinkoff_success(request, pk):
    subdomain = get_subdomain(request)
    try:
        telegram_bot = subdomain.telegram_bot
    except:
        telegram_bot = BaseSettings.objects.get().telegram_bot
    try:
        telegram_group = subdomain.telegram_group
    except:
        telegram_group = BaseSettings.objects.get().telegram_group

    cart = Cart(request)
    cart.combo_clear()
    cart.clear()
    cart.constructor_clear()

    order = Order.objects.get(id=pk)
    order.paid = True
    order.save()
    order_telegram(telegram_bot, telegram_group, order, request)
    
    send_sms(sms_text(order.id, order.summ), order.phone)
    
    return redirect(f'/?order=True&id={order.id}')