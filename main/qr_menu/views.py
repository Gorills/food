from django.shortcuts import render, redirect
from integrations.iiko import create_iiko_order, create_iiko_table
from orders.models import Order, OrderItem
from setup.models import BaseSettings
from shop.models import Category, PickupAreas, Product, Table
# Create your views here.
from admin.views import check_user_rights
import qrcode
from io import BytesIO
from django.core.files import File
from orders.telegram import order_telegram, send_message
from pytils.translit import slugify

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
  
    qr_data = f"https://{domain}/qr_menu/{instance}/{model.id}/"
    
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
    slug = slugify(model.name)
    # Создаем имя файла
    filename = f"qr_{instance}_{slug}.png"
    
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
    products = area.products.all()

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
    products = area.products.all()
    

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

    if table.area.telegram_group:
        tg_group = table.area.telegram_group
    else:
        tg_group = telegram_group


    send_message(telegram_bot, tg_group, f'Вызов официанта от стола {table.name} / {table.area.name}')


    return redirect('table_menu', pk=table.id)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging


# Настройка логгера
logger = logging.getLogger(__name__)


@csrf_exempt  # Отключаем CSRF для POST-запроса (для простоты, в продакшене используйте токен)
def order(request, pk):
    if request.method == 'POST':
        try:
            logger.info(f"Получен запрос для стола с ID {pk}")
            
            # Получаем JSON из тела запроса
            cart_data = json.loads(request.body)
            # logger.debug(f"Данные корзины: {cart_data}")

            # Проверяем существование стола
            table = Table.objects.get(id=pk)
            logger.info(f"Найден стол: {table.name}")
            pickup_area = table.area
            logger.info(f"Pickup area: {pickup_area.address}")

            # Создаем заказ
            order = Order.objects.create(
                phone='+79999999999',
                name='Имя',
                address=pickup_area.address,
                table=table.name,
                table_object=table,
                delivery_method="Самовывоз",
                order_conmment="Заказ из QR-меню. Стол No " + str(pk),
            )
            logger.info(f"Создан заказ с ID {order.id}")

            # Обработка данных корзины
            total = 0
            order_items = []

            for item in cart_data:
                product_id = item['id']
                price = float(item['price'])
                quantity = int(item['quantity'])
                modifiers = item['modifiers']
                
                # logger.debug(f"Обработка товара: id={product_id}, price={price}, quantity={quantity}, modifiers={modifiers}")

                # Подсчет стоимости модификаторов
                modifiers_total = sum(float(mod['price']) for mod in modifiers)
                item_total = (price + modifiers_total) * quantity
                total += item_total

                # Проверяем существование продукта
                product = Product.objects.get(id=product_id)
                logger.info(f"Найден продукт: {product.name}")

                # Создаем элемент заказа
                order_item = OrderItem(
                    order=order,
                    product=product,
                    price=float(item['price']),
                    quantity=int(item['quantity']),
                )
                order_items.append(order_item)
                order_item.save()
                # logger.debug(f"Сохранен элемент заказа: {order_item.id}")


            pickup_area = order.table_object.area if order.table_object else None
            create_iiko_table(order, pickup_area=pickup_area)

            # Формируем сообщение для Telegram
            message = f"**Заказ из QR-меню для стола No{table.name}**\n\n"
            for item in order_items:
                message += f"**{item.product.name}** - {item.quantity} шт.\n"
            # logger.debug(f"Сообщение для Telegram: {message}")

            # Отправка сообщения в Telegram
            if table.area.telegram_group:
                telegram_group = table.area.telegram_group
                logger.info(f"Отправка сообщения в группу: {telegram_group}")
                
            else:
                logger.warning("Telegram-группа не указана для этой зоны самовывоза")

            send_message(telegram_bot, telegram_group, message)

            # Успешный ответ
            return JsonResponse({
                'status': 'success',
                'message': 'Заказ успешно получен',
                'total': total,
                'items': len(order_items)  # Возвращаем количество элементов вместо списка объектов
            })

        except json.JSONDecodeError as e:
            # logger.error(f"Ошибка декодирования JSON: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Некорректный JSON'}, status=400)
        except Table.DoesNotExist:
            # logger.error(f"Стол с ID {pk} не найден")
            return JsonResponse({'status': 'error', 'message': f"Стол с ID {pk} не найден"}, status=404)
        except Product.DoesNotExist as e:
            # logger.error(f"Продукт не найден: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f"Продукт с ID не найден"}, status=404)
        except KeyError as e:
            # logger.error(f"Отсутствует ключ в данных корзины: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f"Отсутствует поле {str(e)} в данных корзины"}, status=400)
        except Exception as e:
            # logger.error(f"Неизвестная ошибка: {str(e)}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        logger.warning(f"Метод {request.method} не поддерживается")
        return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)
    


def order_success(request, pk):

    table = Table.objects.get(id=pk)

    return redirect('table_menu', pk=table.id)