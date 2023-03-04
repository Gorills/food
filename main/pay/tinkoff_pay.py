

from decimal import Decimal
import json
from django.shortcuts import redirect

import requests
from orders.models import OrderItem

from pay.models import Tinkoff

try:
    terminalkey = Tinkoff.objects.get().terminalkey
    taxation = Tinkoff.objects.get().taxation
except:
    terminalkey = ''
    taxation = ''

from setup.models import BaseSettings

try:
    email = BaseSettings.objects.get().email

except:
    email = ''


def create_payment(order, request):
    
    items_arr = []
    
    
    success_url = f'https://{request.META["HTTP_HOST"]}/orders/tinkoff_success/{order.id}/'

    items = OrderItem.objects.filter(order=order)
    
    total = str(order.summ)
    total = total.replace('.', '')

    
    
    for item in items:

        name = item.product.name

        if order.coupon:
            price = item.product.price
            discount = (price/100)*order.discount
            price = price - discount
            price = str(price)
            price = price.replace('.', '')
           

        else:
            price = item.product.price
            price = str(price)
            price = price.replace('.', '')


        quantity = item.quantity
    

        amount = Decimal(price) * Decimal(quantity)
        amount = str(amount)
        amount = amount.replace('.', '')
        
        

        print(item.free)
        print(item.quantity)

        if quantity > item.free:
            items_arr.append({
                
                'Name': name,
                "Price": price,
                "Quantity": quantity,
                "Amount": amount,
                "PaymentMethod": "full_prepayment",
                "PaymentObject": "commodity",
                "Tax": "none",
                })

    

    delivery_price = order.delivery_price

    del_pr = str(delivery_price).replace('.', '')

    if Decimal(delivery_price) > 0:
        items_arr.append({
                
            'Name': 'Доставка',
            "Price": str(del_pr),
            "Quantity": '1',
            "Amount": str(del_pr),
            "PaymentMethod": "full_prepayment",
            "PaymentObject": "commodity",
            "Tax": "none",
            })

    

    

    dictionary = {
        "TerminalKey": terminalkey,
        "Amount": str(total),
        "OrderId": order.id,
        "Description": f"Покупка товаров в магазине {request.META['HTTP_HOST']}",
        "SuccessURL": success_url,
        "Receipt": {
            
            "Phone": order.phone,
            "EmailCompany": email,
            "Taxation": taxation,
            "Items": items_arr
        }
    }
    
    headers = {'content-type': 'application/json'}

    payList = json.dumps(dictionary, indent=4)

    print(payList)

    response = requests.post('https://securepay.tinkoff.ru/v2/Init', headers=headers, data=payList)
    print(response.text)
    res = response.json()
    print(res)
    url = res['PaymentURL']
    

    return url