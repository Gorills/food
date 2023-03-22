

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

import decimal
from decimal import Decimal
D = Decimal
def create_payment(order, request):
    
    items_arr = []
    
    
    success_url = f'https://{request.META["HTTP_HOST"]}/orders/tinkoff_success/{order.id}/'

    items = OrderItem.objects.filter(order=order)
    
    total = str(order.summ)
    total = total.replace('.', '')

    print(total)

    
    # print(items.count())
    
    for item in items:

        try:
            name = item.product.name
        except:
            name = item.combo.name
            
        quantity = item.quantity
        quantity = quantity - item.free


        if order.balls :
           
            price = item.price
            discount = (price/100)*order.percent_pay
            price = price - discount
            price = str(price)
            price = price.replace('.', '')

        else:
           
            price = item.price
            price = str(price)
            price = price.replace('.', '')

        
        

        amount = Decimal(price) * Decimal(quantity)
        amount = str(amount)
        print(amount)
        amount = amount.replace('.', '')

    
        
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
        # print(order.percent_pay)
        # print('Price:')
        # print(price)
        # print('item.free')
        # print(item.free)
        # print('quantity')
        # print(quantity)
        print('Amount:')
        print(amount)



    delivery_price = order.delivery_price

    del_pr = str(Decimal(delivery_price).quantize(D("1.00"))).replace('.', '').replace(',', '')
    
    if Decimal(delivery_price) > 0:

        print(delivery_price)
        items_arr.append({
                
            'Name': 'Доставка',
            "Price": str(del_pr),
            "Quantity": 1,
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
    

    
    # with open('data.json', 'w') as f:
    #     json.dump(payList, f)

    return url