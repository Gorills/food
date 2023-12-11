import requests

# Create your views here.

from .models import Delivery
from setup.models import BaseSettings
from subdomains.utilites import get_protocol
from cart.cart import Cart

api_key = Delivery.objects.get(name='yandex').api_key

city = BaseSettings.objects.get().city
address = BaseSettings.objects.get().address

def get_geo(query):

    
    search_str = f'{city}+{query.replace(" ", "+")}'
    

    geo_url = f'https://geocode-maps.yandex.ru/1.x/?apikey=9cb6c9d2-6eb1-4e15-952e-3f90ae7a078e&geocode={search_str}&format=json'

    response = requests.get(geo_url)

    if response.status_code == 200:
        pos = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

        
        sorted_list = pos.split(' ')
        sorted_pos = [
            float(sorted_list[0]), float(sorted_list[1])
        ]
        

        return sorted_pos

    


# print(get_geo('Трудовая 22/1'))


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


def check_price(quantity):
    url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/check-price'

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept-Language": "ru",
    }

    data = {
        "items": [
            {
            "dropoff_point": 2,
            "quantity": quantity,
            
            }
        ],
        "requirements": {
           
            "cargo_options": [
                "thermobag"
            ],
            
            "pro_courier": False,

            # "same_day_data": {
            #     "delivery_interval": {
            #         "from": "18:00",
            #         "to": "20:00"
            #     }
            # },
            "taxi_class": "express"
        },
        "route_points": [
            {
            "coordinates": get_geo(address),
            "fullname": f'{city}, {address}',
            "id": 1
            },
            {
            "coordinates": [
                 84.932557, 56.522148
                ],
            "fullname": 'Томск, Трудовая 22/1',
            "id": 2
            }
        ],
        "skip_door_to_door": False
        }
    
    print(data)
    
    response = requests.post(url, json=data, headers=headers)

    print(response.json())


# check_price(1)

def create_order(request, order):
    
    items = order.items.all()
    
    
    data = {
        "auto_accept": False,
        "callback_properties": {
            "callback_url": f'Sitemap: {get_protocol(request)}://{request.META["HTTP_HOST"]}/delivery/check_order/'
        },
        "client_requirements": {
            
           
            "cargo_options": [
                "thermobag"
            ],
           
            "pro_courier": False,
            "taxi_class": "express"
        },
        "comment": order.order_conmment,
        # Заказ к конкретному времени
        # "due": string,
        "emergency_contact": {
            "name": order.name,
            "phone": order.phone,
            
        },
        "items": [
            {
            "cost_currency": string,
            "cost_value": string,
            "droppof_point": integer,
            "extra_id": string,
            "fiscalization": {
                "article": string,
                "excise": string,
                "item_type": string,
                "mark": {
                    "code": string,
                    "kind": string
                },
                "supplier_inn": string,
                "vat_code_str": string
            },
            "pickup_point": 1,
            "quantity": integer,
            "size": {
                "height": number,
                "length": number,
                "width": number
            },
            "title": string,
            "weight": number
            }
        ],
        "offer_payload": string,
        "optional_return": boolean,
        "referral_source": string,
        "route_points": [
            {
            "address": {
                "building": string,
                "building_name": string,
                "city": string,
                "comment": string,
                "coordinates": [
                number
                ],
                "country": string,
                "description": string,
                "door_code": string,
                "door_code_extra": string,
                "doorbell_name": string,
                "flat": integer,
                "floor": integer,
                "fullname": string,
                "porch": string,
                "sflat": string,
                "sfloor": string,
                "shortname": string,
                "street": string,
                "uri": string
            },
            "buyout": {
                "payment_method": string
            },
            "contact": {
                "email": string,
                "name": string,
                "phone": string,
                "phone_additional_code": string
            },
            "external_order_cost": {
                "currency": string,
                "currency_sign": string,
                "value": string
            },
            "external_order_id": string,
            "leave_under_door": boolean,
            "meet_outside": boolean,
            "no_door_call": boolean,
            "payment_on_delivery": {
                "customer": {
                "email": string,
                "inn": string,
                "phone": string
                },
                "payment_method": string
            },
            "pickup_code": string,
            "point_id": integer,
            "skip_confirmation": boolean,
            "type": string,
            "visit_order": integer
            }
        ],
        "same_day_data": {
            "delivery_interval": {
            "from": string,
            "to": string
            }
        },
        "shipping_document": string,
        "skip_act": boolean,
        "skip_client_notify": boolean,
        "skip_door_to_door": boolean,
        "skip_emergency_notify": boolean
        }