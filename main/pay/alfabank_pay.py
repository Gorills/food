from decimal import Decimal
from django.shortcuts import render
import requests

from integrations.iiko import create_iiko_order
from .models import PaymentSet, AlfaBank
from orders.models import Order
from shop.models import Product
import json
import threading
import time
from setup.models import BaseSettings
from orders.telegram import order_telegram, send_message

from subdomains.utilites import get_protocol




            

def get_alfa_bank_credentials():
    try:
        alfa_bank = AlfaBank.objects.get()
        return alfa_bank.login, alfa_bank.password, alfa_bank.token
    except AlfaBank.DoesNotExist:
        return '', '', ''

def create_payment(order, cart, request):
    login, password, token = get_alfa_bank_credentials()

    if not login or not password:
        return {'order_id': order.id, 'id': '0', 'confirmation_url': '/pay-error/missing_credentials/'}

    returnUrl = f'{get_protocol(request)}://' + request.META['HTTP_HOST'] + '/orders/success/'
    failUrl = f'{get_protocol(request)}://' + request.META['HTTP_HOST'] + '/orders/error/'

    def dec_to_cop(price):
        res = str(round(price, 2))
        res_filter = res.replace(',', '').replace('.', '')
        return res_filter

    items = []
    count = 1
    for item in order.items.all():
        if item.price != 0:
            product = item.product or item.combo or item.constructor
            i = {
                "positionId": count,
                "name": product.name,
                "quantity": {
                    "value": int(item.quantity),
                    "measure": "шт"
                },
                "itemAmount": dec_to_cop(Decimal(item.price) * item.quantity),
                "itemCode": product.id,
                "itemPrice": dec_to_cop(Decimal(item.price)),
            }
            count += 1
            items.append(i)

    post_data = {
        'userName': login,
        'password': password,
        'orderNumber': order.id,
        'amount': dec_to_cop(order.summ),
        'returnUrl': returnUrl,
        'failUrl': failUrl,
        'dynamicCallbackUrl': f'{get_protocol(request)}://' + request.META['HTTP_HOST'] + '/orders/alfabank_callback/',
        "cartItems": json.dumps(items)  # Сериализуем items в строку JSON
    }

    try:
        r = requests.post("https://payment.alfabank.ru/payment/rest/register.do", post_data)
        r.raise_for_status()
        response_data = r.json()
    except requests.RequestException as e:
        print(f"Error during payment request: {e}")
        return {'order_id': order.id, 'id': '0', 'confirmation_url': '/pay-error/network_error/'}

    confirmation_url = response_data.get('formUrl', '/pay-error/unknown_error/')
    pay_id = response_data.get('orderId', '0')

    data = {
        'order_id': order.id,
        'id': pay_id,
        'confirmation_url': confirmation_url
    }

    return data



try:
    site_name = BaseSettings.objects.get().name
except Exception as e:
    
    site_name = ''

def get_status(pay_id):
    login, password, _ = get_alfa_bank_credentials()
    telegram_bot = BaseSettings.objects.get().telegram_bot
    telegram_group = BaseSettings.objects.get().telegram_group

    try:
        order = Order.objects.get(payment_id=pay_id)
    except Order.DoesNotExist:
        print(f"Order with payment_id {pay_id} does not exist.")
        return {'status': 0, 'order': None}

    post_data = {
        'userName': login,
        'password': password,
        'orderId': pay_id,
        'orderNumber': order.id
    }

    status_pay = 0

    while status_pay not in [2, 6] and not order.order_send_status:
        try:
            r = requests.post("https://payment.alfabank.ru/payment/rest/getOrderStatus.do", post_data)
            r.raise_for_status()
            response_data = r.json()
        except requests.RequestException as e:
            print(f"Error during status request: {e}")
            time.sleep(20)
            continue

        status_pay = response_data.get('OrderStatus', 0)



        if status_pay == 2:
            send_message(wo_elegram_bot, wo_telegram_group, f'Статус оплаты: {status_pay} - {site_name}')
            order.paid = True
            order.save()
            order_telegram(telegram_bot, telegram_group, order)
            # create_iiko_order(order)
        

        time.sleep(20)
        send_message(wo_elegram_bot, wo_telegram_group, f'Статус оплаты: {status_pay} - {site_name}')

    return {'status': status_pay, 'order': order}

def start_background_task(pay_id):
    thread = threading.Thread(target=get_status, args=(pay_id,))
    thread.start()