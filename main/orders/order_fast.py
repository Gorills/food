from django.shortcuts import render, redirect
from accounts.models import LoyaltyCard, LoyaltyCardSettings, UserProfile
import requests
from subdomains.utilites import get_subdomain
from shop.models import Combo, ComboItem, FoodConstructor, Product, ProductOption, ShopSetup
from .models import Order, OrderItem
from .forms import CallbackForm, OrderCreateForm
from cart.cart import Cart
from setup.models import ThemeSettings, BaseSettings
from accounts.models import UserProfile
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from delivery.yandex_eda import yandex_create_order
from django.http import HttpResponse
import json
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

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


if pay_name == 'yookassa':
    from pay.yookassa_pay import create_payment

if pay_name == 'alfabank':
    from pay.alfabank_pay import create_payment, get_status

if pay_name == 'paykeeper':
    from pay.paykeeper_pay import create_payment, get_status

if pay_name == 'tinkoff':
    from pay.tinkoff_pay import create_payment




def order_create(request):
    
    subdomain = get_subdomain(request)

    if subdomain and subdomain.telegram_group:
        telegram_group = subdomain.telegram_group
    else:
        telegram_group = BaseSettings.objects.get().telegram_group
    
    if request.method == 'POST':

        
       

        json_order = json.loads(request.POST['order'])
        
        
        
        if json_order['delivery_method'] == 'Самовывоз':
            address = json_order['address_pickup']
        else:
            address = json_order['address']
        

        try:
            pay_change = Decimal(json_order['pay_change'])

        except:
            pay_change = None

        

        order = Order.objects.create(
            phone = json_order['user_phone'],
            name = json_order['user_name'],
            address = address,
            address_comment = json_order['address_comment'],
            entrance = json_order['entrance'],
            floor = json_order['floor'],
            flat = json_order['flat'],
            door_code = json_order['door_code'],
            time = json_order['day'] + ' / ' + json_order['time'],
            pay_method = json_order['pay_method'],
            pay_change = pay_change,
            delivery_method = json_order['delivery_method'],
            delivery_price = Decimal(json_order['delivery_price']),
            order_conmment = json_order['order_conmment'],
            summ = Decimal(json_order['summ']),


        )

        

        json_cart = json.loads(request.POST['cart'])

        for key, value in json_cart.items():
            
            itemId = value['itemId']
            name = value['name']
            type = value['type']
            price = value['price']
            quantity = value['quantity']
            options = value['options']
            options_name = value['options_name']

            order_item = OrderItem(
                order = order,
                price = price,
                quantity = quantity,

            )

            options_name_str = ''
            for opt in options_name:
                options_name_str = options_name_str + opt['option_value'] + ', '
            options_name_str = options_name_str[:-2]
            

            if type == 'product':
                order_item.product = Product.objects.get(id=itemId)
                order_item.options = options_name_str
            elif type == 'combo':
                order_item.combo = Combo.objects.get(id=itemId)
                order_item.combo_items = options_name_str
            elif type == 'constructor':
                order_item.constructor = FoodConstructor.objects.get(id=itemId)
                order_item.constructor_items = options_name_str

            order_item.save()


        
        

        try:
            user_pr = UserProfile.objects.get(phone=json_order['user_phone'])
        except:
            user_pr = UserProfile.objects.create(phone=json_order['user_phone'])


      
        
        
        # if cart.active_balls:
        #     order.balls = cart.active_balls

        # order.user_pr = user_pr
        # order.summ = cart.get_total_price_after_discount()
        
        # order.delivery_price = Decimal(cart.get_delivery())
        # try:
        #     order.sale_percent = cart.get_discount_on_pickup_persent() + cart.first_delivery
        # except:
        #     order.sale_percent = 0
        

        # # Бонусы сохраняем в заказ
        # if cart.active_balls > 0:
        #     order.bonuses_pay = cart.active_balls
        #     order.percent_pay = cart.percent_pay

        
        # if order.flat:
        #     order.flat = str(order.flat)
        
        

        # order.door_code = domofon
        # order.name = name
        # order.save()
        
        
        cart = []
            

        if json_order['pay_method'] == 'Картой на сайте':

            # отправлять заказ в телеграм бот, даже если не прошла оплата
            info_to_order_anyway = ShopSetup.objects.get().info_to_order_anyway
            
            if info_to_order_anyway:
                order_telegram(telegram_bot, telegram_group, order)


        #     if pay_name == 'yookassa':
        #         data = create_payment(order, cart, request)
        #         payment_id = data['id']
        #         confirmation_url = data['confirmation_url']

        #         order.payment_id = payment_id
        #         order.payment_dop_info = confirmation_url
        #         order.save()
        #         # print(data['path'])
        #         return redirect(confirmation_url)
                
            if pay_name == 'alfabank':

                data = create_payment(order, cart, request)
                payment_id = data['id']
                confirmation_url = data['confirmation_url']

                order.payment_id = payment_id
                order.payment_dop_info = confirmation_url
                order.save()

                # start_background_task(order.payment_id)


                return JsonResponse(data, status=status.HTTP_200_OK)

                # return HttpResponse(data)
                
                

        #     if pay_name == 'paykeeper':

        #         data = create_payment(order, cart, request)
        #         payment_id = data['id']
        #         confirmation_url = data['confirmation_url']
            
        #         # session_url = 'http://' + request.META['HTTP_HOST']+'/orders/paykeeper/session/' + payment_id + '/'
        #         # requests.post(session_url)

        #         order.payment_id = payment_id
        #         order.payment_dop_info = confirmation_url
        #         order.save()
                
        #         print(confirmation_url)
        #         return redirect('/orders/paykeeper/session/' + payment_id + '/')
            
            if pay_name == 'tinkoff':
                data = create_payment(order, request)

                
                order.payment_dop_info = data['url']
                order.payment_id = data['payment_id']
                order.save()

                return redirect(data['url'])



        else:
            order_telegram(telegram_bot, telegram_group, order)

            try:
                send_order_email(order)
            except Exception as e:
                pass
                
            # yandex_create_order(order)
            send_sms(sms_text(order.id, order.summ), order.phone)
            
            # очистка корзины
            
            
            # if LoyaltyCardSettings.objects.get().active == True and BaseSettings.objects.get().sms == True:
            #     user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])

            #     try:
                
            #         loyalty_card = LoyaltyCard.objects.get(user=user_profile)
                
            #     except:
            #         loyalty_card = LoyaltyCard.objects.create(
            #             user=user_profile,
            #             summ=Decimal('0.00')
            #             )

            #     try:
            #         if order.bonuses_pay > 0:
            #             loyalty_card.balls = loyalty_card.balls - order.bonuses_pay

            #     except:
            #         pass
                
            #     loyalty_card.save()

            # request.session['first_delivery'] = 0

            data = {
                'id': order.id,
                'confirmation_url': f'/'
            }

            return JsonResponse(data, status=status.HTTP_200_OK)
        
        
        return HttpResponse("Order created successfully.")
    else:
         return HttpResponse("This view only accepts POST requests.")
  

      
