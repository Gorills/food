import datetime
from decimal import Decimal
from django.http import HttpResponse
import requests

# Create your views here.

from .models import Delivery
from orders.models import Order
from setup.models import BaseSettings
from subdomains.utilites import get_protocol
from cart.cart import Cart


try:
    yandex = Delivery.objects.get(name='yandex')
    api_key = yandex.api_key

    city = yandex.city
    address = yandex.address
    emergency_phone = yandex.phone
    emergency_name = yandex.name
    emergency_email = yandex.email
    delay = yandex.delay
except:
    pass

def format_str_coord(coord):

    coord = coord.split(',')
    sorted_pos = [
        float(coord[1]), float(coord[0])
    ]
    return sorted_pos

def get_geo(query):

    
    search_str = f'{query.replace(" ", "+")}'
    

    geo_url = f'https://geocode-maps.yandex.ru/1.x/?apikey=b0ace043-1020-4411-ac5e-80354ec8241c&geocode={search_str}&format=json'

    response = requests.get(geo_url)

    if response.status_code == 200:
        pos = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

        
        sorted_list = pos.split(' ')
        sorted_pos = [
            float(sorted_list[0]), float(sorted_list[1])
        ]
        
        
        return sorted_pos

    


# print(get_geo('Томск, Ленина 210'))


def delivery_methods():
    url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/delivery-methods'
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept-Language": "ru",
    }

    string = f'{city} {address}'

    data = {
        
        "fullname": string,
        "start_point": [56.504537, 84.948083],
       
    }

    response = requests.post(url, json=data, headers=headers)

    print(response.json())



# delivery_methods()

def get_due():

    now_time = datetime.datetime.now()

    

    # Добавить задержку к текущему времени
    delay_time = datetime.timedelta(minutes=60)
    new_time = now_time

    # Форматировать новое время и время задержки в строку в нужном формате (ISO 8601)
    formatted_time = new_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    formatted_delay = delay_time.seconds // 3600, (delay_time.seconds % 3600) // 60

    due = f'{formatted_time}+{formatted_delay[0]:02d}:{formatted_delay[1]:02d}'


    return due



def check_price(request):
    # Получить текущее время
    

    if request.method == 'POST':
        dotaddress = request.POST['dotaddress']
    

        url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/check-price'

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept-Language": "ru",
        }

        data = {
            
            "requirements": {
            
                "cargo_options": [
                    "thermobag"
                ],
                
                "pro_courier": False,
              
                "taxi_class": "express"
            },
            "route_points": [
                {
                "coordinates": format_str_coord(yandex.adress_dot),
                "fullname": f'{city}, {address}',
                "id": 1
                },
                {
                "coordinates": get_geo(dotaddress),
                    
                "fullname": f'{dotaddress}',
                "id": 2
                }
            ],
            "skip_door_to_door": False,
            'due': get_due(),
            }
        
        
        
        response = requests.post(url, json=data, headers=headers)
        

        
        return HttpResponse(response, content_type='application/json') 


# check_price('Томск, проспект Ленина, 1')


def yandex_create_order(order):

    try:
    
        items = order.items.all()
        items_list = []
        
        for item in items:

            add_item = {
                "cost_currency": "RUB",
                "cost_value": str(item.price),
                "droppof_point": 2,
                "extra_id": str(item.order.id),

                
                "pickup_point": 1,
                "quantity": item.quantity,
                
            }

            if item.product:
                add_item['title'] = item.product.name
            elif item.combo:
                add_item['title'] = item.combo.name
            if item.weight:
                grams = float(''.join(c for c in item.weight if c.isdigit() or c == '.'))
                kilograms = grams / 1000.0

                add_item['weight'] = kilograms

            items_list.append(add_item)
            
        
        

        
        data = {
            "auto_accept": False,
            # "callback_properties": {
            #     "callback_url": f'{get_protocol(request)}://{request.META["HTTP_HOST"]}/delivery/check_order/'
            # },
            "client_requirements": {
                
            
                "cargo_options": [
                    "thermobag"
                ],
            
                "pro_courier": False,
                "taxi_class": "express"
            },
            "comment": '',
            
            "emergency_contact": {
                "name": emergency_name,
                "phone": emergency_phone,
                
            },
            "items": items_list,
        
            "optional_return": False,
            
            "route_points": [
                {
                    "address": {
                        
                        "city": city,
                        "comment": yandex.comment,
                        "coordinates": format_str_coord(yandex.adress_dot),
                        "country": 'Россия',
                        
                        
                        
                        
                        "floor": int(yandex.floor),
                        "fullname": f'{yandex.city}, {yandex.address}',
                        
                        "street": yandex.address,
                        
                    },
                    
                    "contact": {
                        "email": yandex.email,
                        "name": yandex.name,
                        "phone": str(yandex.phone).replace(' ', '').replace('-', '').replace('(', '').replace(')', ''),
                        
                    },
                    
                    # "external_order_id": string,
                    "leave_under_door": False,
                    "meet_outside": False,
                    "no_door_call": False,
                    
                    
                    "point_id": 1,
                    "skip_confirmation": True,
                    "type": 'source',
                    "visit_order": 1
                },
                {
                    "address": {
                        
                        
                        "city": city,
                        "comment": order.address_comment,
                        "coordinates": get_geo(order.address),
                        "country": 'Россия',
                    
                        "door_code": order.door_code,
                    
                    
                        "flat": int(order.flat),
                        "floor": int(order.floor),
                        "fullname": order.address,
                        
                    },
                    
                    "contact": {
                    
                        "name": order.name,
                        "phone": str(order.phone).replace(' ', '').replace('-', '').replace('(', '').replace(')', ''),
                    
                    },
                    
                    "external_order_id": str(order.id),
                    "leave_under_door": False,
                    "meet_outside": False,
                    "no_door_call": False,
                    
                    
                    "point_id": 2,
                    "skip_confirmation": True,
                    "type": 'destination',
                    "visit_order": 2
                    }
            ],
            # "same_day_data": {
            #     "delivery_interval": {
            #         "from": string,
            #         "to": string
            #     }
            # },
            
            "skip_act": True,
            "skip_client_notify": False,
            "skip_door_to_door": False,
            'due': get_due(),
            "skip_emergency_notify": False
            }
        

        

        # order_time_list = order.time.split('/')
        

        # monthes = {
        #     'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
        #     'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
        #     'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
        # }

        # if order_time_list[0] != 'Как можно скорее':

        #     times = order_time_list[0].split('-')
        #     data['same_day_data'] = {
        #         "delivery_interval": {
        #             "from": times[0],
        #             "to": times[1]
        #         }
        #     }
            
        #     if order_time_list[1].replace(' ', '') == 'Сегодня':
        #         day = datetime.datetime.now().day
        #         month = datetime.datetime.now().month
        #         year_number = datetime.datetime.now().year
        #         now_date = datetime.datetime(year_number, month, int(day))
        #         result = now_date.strftime("%d.%m.%Y")
        #         data['due'] = result

        #     else:
        #         day, month = str(order_time_list[1].replace('Завтра, ', '')).split()
        #         month_number = monthes[month.lower()]
        #         year_number = datetime.datetime.now().year

        #         now_date = datetime.datetime(year_number, month_number, int(day))
        #         result = now_date.strftime("%d.%m.%Y")
        #         data['due'] = result
                

        

        # if order_time_list[1].replace(' ', '') != 'Сегодня':
        #     data['due'] = order_time_list[1].replace('Завтра, ', '')
            
        
        print(data)
        url = f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/create?request_id={order.id}'

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept-Language": "ru",
        }

        response = requests.post(url, json=data, headers=headers)

        print(response.json())
    except Exception as e:
        print(e)


yandex_create_order(Order.objects.get(id=61))