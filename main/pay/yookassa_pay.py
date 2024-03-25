from decimal import Decimal
from django.shortcuts import render

from .models import PaymentSet, Yookassa
from shop.models import Product, Combo, ProductOption
from subdomains.utilites import get_protocol
from setup.models import ThemeSettings, BaseSettings
# Create your views here.
from yookassa import Configuration, Payment

try:
    Configuration.account_id = Yookassa.objects.get().shop_id
    Configuration.secret_key = Yookassa.objects.get().key
except:
    Configuration.account_id = ''
    Configuration.secret_key = ''

try:
    telegram_bot = BaseSettings.objects.get().telegram_bot
    telegram_group = BaseSettings.objects.get().telegram_group
except Exception as e:
    
    telegram_bot = ''
    telegram_group = ''

from orders.telegram import order_telegram

def create_payment(order, cart, request):

    path = f'{get_protocol(request)}://' + request.META['HTTP_HOST']
    
    items = []

    

    phone = order.phone

    digits_only = ''.join(char for char in phone if char.isdigit())
    
    sale_percent = order.sale_percent
    
    for item in order.items.all():
        

        if item.product:
            product = item.product
        elif item.combo:
            product = item.combo
        elif item.constructor:
            product = item.constructor
        
        price = str(Decimal(item.price) - (Decimal(item.price/100) * sale_percent))

        i = {
            "description": product.name,
            "quantity": int(item.quantity),
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "vat_code": Yookassa.objects.get().vat_code,
            "payment_mode": "full_payment",
            "payment_subject": "commodity"
        }
        
        items.append(i)

    

    if order.delivery_method == 'Доставка':
        delivery = {
            "description": 'Доставка',
            "quantity": 1,
            "amount": {
                "value": order.delivery_price,
                "currency": "RUB"
            },
            "vat_code": Yookassa.objects.get().vat_code,
            "payment_mode": "full_payment",
            "payment_subject": "commodity"
        }
        items.append(delivery)

    payment = Payment.create({
        "amount": {
            "value": str(order.summ),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": path+"/orders/confirm/" + str(order.id)
        },
        "capture": True,
        "description": "Заказ №" + str(order.id),
        "metadata": {
        "order_id": str(order.id)
        }, 
        "receipt": {
            "customer": {
                "full_name": order.name,
                "phone": str(digits_only)
            },
            "items": items
        }
    })

    data = {
        'id': payment.id,
        'order_id': order.id,
        'confirmation_url': payment.confirmation.confirmation_url,
        'path': path
        
    }

    print(data)
    # order_telegram(telegram_bot, telegram_group, data)
    return data


