import requests

# Create your views here.

from .models import Delivery
from setup.models import BaseSettings


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
            float(sorted_list[1]), float(sorted_list[0])
        ]
        

        return sorted_pos

    


# print(get_geo('Ленина 210'))


def delivery_methods(query):
    url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/check-price'
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept-Language": "ru",
    }

    string = f'{city} {address}'

    data = {
        
        "fullname": string,
        "start_point": get_geo(query)
       
    }

    response = requests.post(url, json=data, headers=headers)

    print(response.json())



# delivery_methods('Ленина 210')