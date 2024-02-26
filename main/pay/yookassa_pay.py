from decimal import Decimal
from django.shortcuts import render

from .models import PaymentSet, Yookassa
from shop.models import Product, Combo, ProductOption
from subdomains.utilites import get_protocol

# Create your views here.
from yookassa import Configuration, Payment

try:
    Configuration.account_id = Yookassa.objects.get().shop_id
    Configuration.secret_key = Yookassa.objects.get().key
except:
    Configuration.account_id = ''
    Configuration.secret_key = ''

def create_payment(order, cart, request):

    path = f'{get_protocol(request)}://' + request.META['HTTP_HOST']
    
    items = []

    

    phone = order.phone

    digits_only = ''.join(char for char in phone if char.isdigit())
    
    sale_percent = order.sale_percent
    print(sale_percent)
    for item in cart:
        product = Product.objects.get(id=item['product'].id)
        
        price = str(Decimal(item['price']) - (Decimal(item['price']/100) * sale_percent))

        i = {
            "description": product.name,
            "quantity": int(item['quantity']),
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "vat_code": Yookassa.objects.get().vat_code,
            "payment_mode": "full_payment",
            "payment_subject": "commodity"
        }
        
        items.append(i)

    for item in cart.get_combos():
        price = str(Decimal(item['price']) - (Decimal(item['price']/100) * sale_percent))
        i = {
            "description": item['combo'].name,
            "quantity": int(item['quantity']),
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "vat_code": Yookassa.objects.get().vat_code,
            "payment_mode": "full_payment",
            "payment_subject": "commodity"
        }
        items.append(i)
    
    for item in cart.get_options():
        price = str(Decimal(item['price']) - (Decimal(item['price']/100) * sale_percent))
        i = {
            "description": item['products'].name,
            "quantity": int(item['quantity']),
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "vat_code": Yookassa.objects.get().vat_code,
            "payment_mode": "full_payment",
            "payment_subject": "commodity"
        }
        items.append(i)



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
        'confirmation_url': payment.confirmation.confirmation_url,
        'path': path
        
    }

    print(data)

    return data


