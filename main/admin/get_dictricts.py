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

    return result


# areaCoordsParser('Советский район, Красноярск')

from setup.models import BaseSettings


def get_file(data_rions):
    city = BaseSettings.objects.get().city
    site = BaseSettings.objects.get().name

    colors = {
        

        'five': '#595959',
        'four': '#b51eff',
        'three': '#ed4543',
        'two': '#1e98ff',
        'one': '#1bad03',
    }

    rions = data_rions.split(';')

    features = []
    counter = 0
    sorted_rions = sorted(rions, key=lambda x: int(x.split(',')[1]))

    for region in sorted_rions:
        str_list = region.split(',')
        try:
            result = areaCoordsParser(f'{str_list[0]} район, {city}, Россия')
            color_index = min(int(str_list[1]), len(colors) - 1)
            fill_color = list(colors.values())[color_index]
            stroke_color = list(colors.values())[color_index]

            try:
                str_list_3 = str_list[3]
            except:
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
                    "fill": fill_color,
                    "fill-opacity": 0.4,
                    "stroke": stroke_color,
                    "stroke-width": "1",
                    "stroke-opacity": 0.4
                }
            })
            counter += 1
        except:
            pass

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "name": site,
            "creator": "Yandex Map Constructor"
        },
        "features": features
    }

    with open('../core/result.geojson', 'w') as f:
        json.dump(geojson, f)

    


# get_file('result.geojson')