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



def create_payment(order, cart, request):

    returnUrl = 'https://' + request.META['HTTP_HOST']+'/orders/success/'
    failUrl = 'https://' + request.META['HTTP_HOST']+'/orders/error/'

    def dec_to_cop(price):

        res = str(round(price, 2))
        res_filter = res.replace(',', '').replace('.', '')
        return res_filter

    items = []
    count = 1
    for item in cart:
        product = Product.objects.get(id=item['product'].id)
        i = {
            "positionId":count,
            "name":product.name,
            "quantity":
                {
                    "value":int(item['quantity']),
                    "measure":"шт"
                },
            "itemAmount":dec_to_cop(Decimal(item['price'])*item['quantity']),
            "itemCode":product.id,
            "itemPrice":dec_to_cop(Decimal(item['price'])),
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

    r = requests.post("https://web.rbsuat.com/ab/rest/register.do", post_data) 
    print(r.json())

    try:
        confirmation_url = r.json()['formUrl']
        pay_id = r.json()['orderId']
    except:
        error = r.json()['errorCode']
        confirmation_url = '/pay-error/'+error+'/'
        pay_id = '0'

   

    data = {
        'id': pay_id,
        'confirmation_url': confirmation_url
    }


    return data
   



def get_status(pay_id):

    order = Order.objects.get(payment_id=pay_id)

    post_data={
        'userName': login, 
        'password': password, 
        'orderId': pay_id,
        'orderNumber': order.id
            
    }

    r = requests.post("https://web.rbsuat.com/ab/rest/getOrderStatusExtended.do", post_data) 

    status = r.json()['errorCode']  

    data = {
        'status': status,
        'order': order
    }


    return data    





