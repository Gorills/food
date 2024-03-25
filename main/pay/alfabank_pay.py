from decimal import Decimal
from django.shortcuts import render
import requests
from .models import PaymentSet, AlfaBank
from orders.models import Order
from shop.models import Product

try:
    login = AlfaBank.objects.get().login
    password = AlfaBank.objects.get().password
    token = AlfaBank.objects.get().token
except:
    login = ''
    password = ''
    token = ''

gateway_url = ''


from subdomains.utilites import get_protocol

def create_payment(order, cart, request):

    returnUrl = f'{get_protocol(request)}://' + request.META['HTTP_HOST']+'/orders/success/'
    failUrl = f'{get_protocol(request)}://' + request.META['HTTP_HOST']+'/orders/error/'

    def dec_to_cop(price):

        res = str(round(price, 2))
        res_filter = res.replace(',', '').replace('.', '')
        return res_filter

    items = []
    count = 1
    for item in order.items.all():

        if item.product:
            product = item.product
        elif item.combo:
            product = item.combo
        elif item.constructor:
            product = item.constructor

        
        i = {
            "positionId":count,
            "name":product.name,
            "quantity":
                {
                    "value":int(item.quantity),
                    "measure":"шт"
                },
            "itemAmount":dec_to_cop(Decimal(item.price)*item.quantity),
            "itemCode":product.id,
            "itemPrice":dec_to_cop(Decimal(item.price)),
            }
        count += 1
        items.append(i)


   

    post_data={
        'userName': login, 
        'password': password, 
        'orderNumber': order.id,
        'amount': dec_to_cop(order.summ),
        'returnUrl': returnUrl,
        'failUrl': failUrl,

        "cartItems": items
            
    }
    
    r = requests.post("https://payment.alfabank.ru/payment/rest/register.do", post_data) 
    print(r.json())

    try:
        confirmation_url = r.json()['formUrl']
        pay_id = r.json()['orderId']
    except:
        error = r.json()['errorCode']
        confirmation_url = '/pay-error/'+error+'/'
        pay_id = '0'

   

    data = {
        'order_id': order.id,
        'id': pay_id,
        'confirmation_url': confirmation_url
    }


    return data
   


import threading
import time
from setup.models import BaseSettings
from orders.telegram import order_telegram, send_message
from delivery.yandex_eda import yandex_create_order

def get_status(pay_id):

    telegram_bot = BaseSettings.objects.get().telegram_bot
    telegram_group = BaseSettings.objects.get().telegram_group

    order = Order.objects.get(payment_id=pay_id)

    post_data={
        'userName': login, 
        'password': password, 
        'orderId': pay_id,
        'orderNumber': order.id
            
    }

    status = order.paid
    r = requests.post("https://payment.alfabank.ru/payment/rest/getOrderStatus.do", post_data) 
    status_pay = r.json()['OrderStatus']  

    telegram_bot_work = '5922674089:AAFxcjyYfti0ypSINOSP9jMz74RloWpmPPs'
    telegram_group_work = '-1001850576262'
    
    count = 0
    while status == False and status_pay != 2:
        if status_pay == 6 or count == 48:

            message = f'Статус оплаты: {status_pay}, сайт: {BaseSettings.objects.get().name}, Счетчик: {count}'
            
            send_message(telegram_bot_work, telegram_group_work, message)
            break
        else:
            r = requests.post("https://payment.alfabank.ru/payment/rest/getOrderStatus.do", post_data) 
            # print(r.json())
            status_pay = r.json()['OrderStatus']  

        if status_pay == 2:
            status = True
            order.paid = True
            order.save()
            

            order_telegram(telegram_bot, telegram_group, order)
            yandex_create_order(order)

            message = f'Статус оплаты: {status_pay}, сайт: {BaseSettings.objects.get().name}, Счетчик: {count}'
        
            send_message(telegram_bot_work, telegram_group_work, message)
            break
        
        count +=1
        time.sleep(20)

        message = f'Статус оплаты: {status_pay}, сайт: {BaseSettings.objects.get().name}, Счетчик: {count}'
      
        send_message(telegram_bot_work, telegram_group_work, message)
        # print(status_pay)
        # print(count)



    data = {
        'status': status_pay,
        'order': order
    }


    return data

    


    






def start_background_task(pay_id):
    thread = threading.Thread(target=get_status, args=(pay_id, ))
    thread.start()
