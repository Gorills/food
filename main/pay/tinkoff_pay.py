

from decimal import Decimal, ROUND_HALF_UP

import json
from django.shortcuts import redirect

import requests
from orders.models import OrderItem, Order

from pay.models import Tinkoff

try:
    terminalkey = Tinkoff.objects.get().terminalkey
    taxation = Tinkoff.objects.get().taxation
    password = Tinkoff.objects.get().password
except:
    terminalkey = ''
    taxation = ''
    password = ''

from setup.models import BaseSettings

try:
    email = BaseSettings.objects.get().email

except:
    email = ''
from subdomains.utilites import get_protocol



D = Decimal
import hashlib

def integer_to_decimal_with_precision(integer_value, precision=2):
    decimal_value = Decimal(integer_value)
    decimal_value = decimal_value.quantize(Decimal('0.1') ** precision, rounding=ROUND_HALF_UP)
    return decimal_value


def create_payment(order, request):
    
    items_arr = []
    
    
    success_url = f'{get_protocol(request)}://{request.META["HTTP_HOST"]}/orders/tinkoff_success/{order.id}/'

    items = OrderItem.objects.filter(order=order)
    
    total = integer_to_decimal_with_precision(order.summ)

    
    total = str(Decimal(total)).replace('.', '')

    

    # print('Скидка: ' + str(order.sale_percent))
    # print('total: ' + str(total))

    
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
           
            price = item.price - (item.price / 100 * order.sale_percent)
            price = str(price)
            price = price.replace('.', '')

        
        

        amount = Decimal(price) * Decimal(quantity)
        amount = str(amount)
        # print(amount)
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
        # print('Amount:')
        # print(amount)



    delivery_price = order.delivery_price

    del_pr = str(Decimal(delivery_price).quantize(D("1.00"))).replace('.', '').replace(',', '')


    token = [{"Amount": f"{total}"},{"Description": "Покупка товаров в магазине"},{"OrderId": f"{order.id}"},{"Password": f"{password}"},{"TerminalKey": f"{terminalkey}"}]
    
    print(token)
    
    # Конкатенация значений пар в одну строку
    concatenated_string = ''.join([list(item.values())[0] for item in token])

    print(concatenated_string)

    # Применение хеш-функции SHA-256
    hashed_value = hashlib.sha256(concatenated_string.encode('utf-8')).hexdigest()

    print(hashed_value)
        
    if Decimal(delivery_price) > 0:

        # print(delivery_price)
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
        "Description": f"Покупка товаров в магазине",
        "SuccessURL": success_url,
        "Receipt": {
            
            "Phone": order.phone,
            "EmailCompany": email,
            "Taxation": taxation,
            "Items": items_arr
        },
        # "Token": hashed_value
    }
    
    headers = {'content-type': 'application/json'}

    payList = json.dumps(dictionary, indent=4)


    
    

    response = requests.post('https://securepay.tinkoff.ru/v2/Init', headers=headers, data=payList)
    print(response.text)
    res = response.json()
    
    url = res['PaymentURL']
    payment_id = res['PaymentId']

    # print(payment_id)
    
    data = {
        'order_id': order.id,
        'confirmation_url': url,
        'hashed_value': hashed_value,
        'payment_id': payment_id
    }

    
    # with open('data.json', 'w') as f:
    #     json.dump(payList, f)

    return data



def get_status(pay_id):
    headers = {'content-type': 'application/json'}

    url = "https://securepay.tinkoff.ru/v2/CheckOrder"

    order = Order.objects.get(payment_id=pay_id)
    token = order.payment_dop_info

    data = {
        "TerminalKey": terminalkey,
        "PaymentId": pay_id,
        "Token": token
    }

    get_status = requests.post(url, headers=headers, data=data)

    print(token)

    print(get_status.content)
    

# get_status('4311736054')