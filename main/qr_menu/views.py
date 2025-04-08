from django.shortcuts import render, redirect
from setup.models import BaseSettings
from shop.models import Category, PickupAreas, Product, Table
# Create your views here.
from admin.views import check_user_rights
import qrcode
from io import BytesIO
from django.core.files import File
from orders.telegram import send_message


try:
    telegram_bot = BaseSettings.objects.get().telegram_bot
    telegram_group = BaseSettings.objects.get().telegram_group
except Exception as e:
    
    telegram_bot = '5922674089:AAFxcjyYfti0ypSINOSP9jMz74RloWpmPPs'
    telegram_group = '-1001850576262'


def generate_qr_code(model, instance, domain=None):
    """Генерирует QR-код с ссылкой на стол"""
    # Если домен не передан, используем заглушку
    if not domain:
        domain = "example.com"  # Можно заменить на значение по умолчанию
    
    # Формируем URL
    qr_data = f"https://{domain}/qr_menu/area/{model.id}/"
    
    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Создаем изображение QR-кода
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Сохраняем изображение в памяти
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Создаем имя файла
    filename = f"qr_table_{model.id}.png"
    
    # Сохраняем QR-код в поле модели
    model.qr_code.save(filename, File(buffer), save=False)
    buffer.close()
    model.save()



@check_user_rights(['view_all_statictic'])
def qr_menu(request):

    areas = PickupAreas.objects.all()

    context = {
        'areas': areas
    }


    return render(request, 'qr_menu/qr_menu.html', context)


@check_user_rights(['view_all_statictic'])
def generate_area_qr(request, pk):
    

    area = PickupAreas.objects.get(id=pk)
    domain = request.get_host()  # Получаем домен из request
    generate_qr_code(area, 'area', domain=domain)

    
    return redirect('qr_menu')



@check_user_rights(['view_all_statictic'])
def generate_table_qr(request, pk):
    
    table = Table.objects.get(id=pk)
    domain = request.get_host()  # Получаем домен из request
    generate_qr_code(table, 'table', domain=domain)

    
    return redirect('qr_menu')

from django.db import models
def area_menu(request, pk):
    area = PickupAreas.objects.get(id=pk)
    products = area.product_set.all()

    # Получаем уникальные категории
    categories_set = set()
    for product in products:
        if product.parent:
            categories_set.add(product.parent)
        categories_set.update(product.parent_add.all())

    # Создаем словарь категорий с их продуктами
    categories_with_products = {}
    for cat in categories_set:
        # Фильтруем продукты, где категория является либо parent, либо в parent_add
        cat_products = products.filter(
            models.Q(parent=cat) | models.Q(parent_add__in=[cat])
        ).distinct()
        categories_with_products[cat] = cat_products

    context = {
        'area': area,
        'products': products,  # Все продукты для области (если нужно)
        'categories_with_products': categories_with_products,  # Категории с продуктами
    }

    return render(request, 'qr_menu/qr_area.html', context)



def table_menu(request, pk):

    table = Table.objects.get(id=pk)
    area = table.area
    products = area.product_set.all()
    

    # Получаем уникальные категории
    categories_set = set()
    for product in products:
        if product.parent:
            categories_set.add(product.parent)
        categories_set.update(product.parent_add.all())

    # Создаем словарь категорий с их продуктами
    categories_with_products = {}
    for cat in categories_set:
        # Фильтруем продукты, где категория является либо parent, либо в parent_add
        cat_products = products.filter(
            models.Q(parent=cat) | models.Q(parent_add__in=[cat])
        ).distinct()
        categories_with_products[cat] = cat_products

    context = {
        'table': table,
        'area': area,
        'products': products,  # Все продукты для области (если нужно)
        'categories_with_products': categories_with_products,  # Категории с продуктами
    }

    return render(request, 'qr_menu/qr_area.html', context)




def oficiant_call(request, pk):
    table = Table.objects.get(id=pk)


    send_message(telegram_bot, telegram_group, f'Вызов официанта от стола {table.name} / {table.area.name}')


    return redirect('table_menu', pk=table.id)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Отключаем CSRF для POST-запроса (для простоты, в продакшене используйте токен)
def order(request):
    if request.method == 'POST':
        try:
            # Получаем JSON из тела запроса
            cart_data = json.loads(request.body)
            print("Полученные данные корзины:", cart_data)  # Для отладки

            # Пример структуры cart_data:
            # [
            #     {"id": "1", "name": "Пицца", "price": 500, "quantity": 2, "modifiers": [{"id": "mod1", "name": "Соус", "price": 15}], "image": "/path/to/image.webp"},
            #     {"id": "2", "name": "Салат", "price": 300, "quantity": 1, "modifiers": [], "image": "/path/to/image2.webp"}
            # ]

            # Обработка данных корзины
            total = 0
            order_items = []

            for item in cart_data:
                product_id = item['id']
                name = item['name']
                price = float(item['price'])
                quantity = int(item['quantity'])
                modifiers = item['modifiers']
                image = item.get('image', '')  # Может быть пустым

                # Подсчет стоимости модификаторов
                modifiers_total = sum(float(mod['price']) for mod in modifiers)
                item_total = (price + modifiers_total) * quantity
                total += item_total

                # Формируем данные для заказа (можно сохранить в БД)
                order_items.append({
                    'product_id': product_id,
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'modifiers': modifiers,
                    'image': image,
                    'item_total': item_total
                })

            # Здесь можно сохранить заказ в базу данных
            # Например:
            # order = Order.objects.create(total=total)
            # for item in order_items:
            #     OrderItem.objects.create(order=order, product_id=item['product_id'], quantity=item['quantity'], ...)

            # Возвращаем успешный ответ
            return JsonResponse({
                'status': 'success',
                'message': 'Заказ успешно получен',
                'total': total,
                'items': order_items
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некорректный JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)
    


def order_success(request, pk):

    table = Table.objects.get(id=pk)
    
    return redirect('table_menu', pk=table.id)