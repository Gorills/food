import json
import urllib.parse
import urllib.request

from django.shortcuts import redirect


def areaCoordsParser(search):
    query = urllib.parse.urlencode({
        'format': 'json',
        'q': search,
        'polygon_geojson': 1
    })
    url = f"http://nominatim.openstreetmap.org/search?{query}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    result = []
    
    


    if data[0]['geojson']['type'] == 'MultiPolygon':
        coords = data[0]['geojson']['coordinates']
        for coord in coords:
            temp = []
            for item in coord[0]:
                temp.append(list(reversed(item[::-1])))
            result.append(temp)
        print('MultiPolygon')
    elif data[0]['geojson']['type'] == 'Polygon':
        coords = data[0]['geojson']['coordinates'][0]
        for coord in coords:
            result.append(list(reversed(coord[::-1])))


    def get_nested_depth(result):
        if isinstance(result, list):  # Проверяем, является ли элемент массивом
            if len(result) == 0:  # Если массив пустой, то его глубина вложенности 1
                return 1
            else:
                depths = [get_nested_depth(item) for item in result]  # Рекурсивно вызываем функцию для каждого элемента
                return max(depths) + 1  # Возвращаем максимальную глубину вложенности элементов плюс 1
        else:
            return 0  # Если элемент не является массивом, то его глубина вложенности 0

    depth = get_nested_depth(result)
    if depth <= 2:
        result = [result]  # Обернуть массив в []

    print(result)

    return result


# areaCoordsParser('Санкт-Петербург Кировский район')

from setup.models import BaseSettings

import random

def get_random_color(used_colors):
    # Предопределенная палитра цветов
    color_palette = [
        '#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1',
        '#955251', '#B565A7', '#009B77', '#DD4124', '#45B8AC',
        '#EFC050', '#1F3A93', '#FF8C69', '#5E2D79', '#D94F70',
        '#7BC4C4', '#E3B23C', '#6A5ACD', '#E6A9EC', '#2E8B57'
    ]
    
    # Удаляем уже использованные цвета
    available_colors = [color for color in color_palette if color not in used_colors]
    
    # Если закончились цвета, генерируем случайный HEX
    if not available_colors:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    # Выбираем случайный цвет из доступных
    return random.choice(available_colors)

def get_file(data_rions):
    city = BaseSettings.objects.get().city
    site = BaseSettings.objects.get().name

    rions = data_rions.split(';')
    features = []
    counter = 0
    used_colors = set()  # Множество для отслеживания использованных цветов

    for region in rions:
        str_list = region.split(',')
        try:
            result = areaCoordsParser(f'{str_list[0]}')
            # Получаем случайный цвет, которого еще не было
            color = get_random_color(used_colors)
            used_colors.add(color)  # Добавляем цвет в использованные

            try:
                str_list_3 = str_list[3]
            except IndexError:
                str_list_3 = ''
            features.append({
                "type": "Feature",
                "id": counter,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": result
                },
                "properties": {
                    "description": f"{str_list[1]}:{str_list[2].replace(' ', '')}:{str_list_3.replace(' ', '')}",
                    "fill": color,
                    "fill-opacity": 0.4,
                    "stroke": color,
                    "stroke-width": "1",
                    "stroke-opacity": 0.4
                }
            })
            counter += 1
        except Exception as e:
            print(f"Ошибка обработки региона {str_list[0]}: {e}")
            pass

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "name": site,
            "creator": "Yandex Map Constructor"
        },
        "features": features
    }

    try:
        with open('../core/result.geojson', 'w', encoding='utf-8') as f:
            json.dump(geojson, f)
    except:
        with open('core/result.geojson', 'w', encoding='utf-8') as f:
            json.dump(geojson, f)
    


# get_file('Санкт-Петербург Кировский район, 0, 999999; Санкт-Петербург Красносельский район, 0, 5000; Санкт-Петербург Московский район, 0, 999999; Санкт-Петербург Невский район, 0, 999999; Санкт-Петербург Центральный район, 0, 10000; Санкт-Петербург Фрунзенский район, 0, Фрунзенский; Санкт-Петербург Приморский район, 0, 10000; Санкт-Петербург Адмиралтейский район, 0, 10000; Санкт-Петербург Василеостровский район, 0, 10000; Санкт-Петербург Петроградский район, 0, 999999; Санкт-Петербург Петродворцовый район, 0, 999999;')