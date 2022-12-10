from decimal import Decimal
from django.shortcuts import render
import requests
from .models import PaymentSet, PayKeeper
from orders.models import Order
from shop.models import Product
from http.client import HTTPSConnection
from base64 import b64encode


try:
    login = PayKeeper.objects.get().login
    password = PayKeeper.objects.get().password
    server = PayKeeper.objects.get().server
    if server[-1] == '/':
        server = server[:-1]
   
except:
    login = ''
    password = ''
    server = ''

    
def basic_auth(login, password):
    token = b64encode(f"{login}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


headers={
    "Content-Type":"application/x-www-form-urlencoded",
    'Authorization' : basic_auth(login, password)
    }


info = server + '/info/settings/token/'
pay_url = server + '/change/invoice/preview/'



def create_payment(order, cart, request):


    get_token = requests.get(info, headers=headers)
    token = get_token.json()['token']

    post_data = {
        "pay_amount": order.summ,
        "orderid": order.id,
        
        "client_phone": order.phone,
        'token': token

    }
    
    

    get_url = requests.post(pay_url, post_data, headers=headers)

    data = {
        'id': get_url.json()['invoice_id'],
        'confirmation_url': server + '/bill/' + get_url.json()['invoice_id'] + '/'
    }

    return(data)




def get_status(pay_id):

    order = Order.objects.get(payment_id=pay_id)
    get_status = requests.get(server + '/info/invoice/byid/?id=' + str(pay_id), headers=headers)
    status = get_status.json()['status']

    print(get_status.content)
    

    data = {
        'status': status,
        'order': order
        
    }

    return(data)










