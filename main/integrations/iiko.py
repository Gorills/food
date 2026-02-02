from decimal import Decimal
import re
import requests
import uuid
import threading
import time
from orders.telegram import send_message
from orders.models import Order

# Create your views here.
import logging
from .models import Integrations


from pytils.translit import slugify
from django.core.files.base import ContentFile
from shop.models import Category, OptionImage, OptionType, Product, ProductOption, PickupAreas
import json


logger = logging.getLogger(__name__)


def get_iiko_integration():
    """Возвращает запись интеграции iiko или None, если её нет."""
    try:
        return Integrations.objects.get(name='iiko')
    except Integrations.DoesNotExist:
        return None


def get_iiko_api_key(pickup_area=None):
    """
    Возвращает api_key для iiko: из pickup_area или из глобальной интеграции.
    Возвращает None, если интеграция не настроена или api_key пустой.
    """
    if pickup_area and getattr(pickup_area, 'api_key', None):
        key = pickup_area.api_key
        return key.strip() or None
    integration = get_iiko_integration()
    if integration:
        key = getattr(integration, 'api_key', None)
        return key.strip() if key else None
    return None


def token(api_key):
    """Получение токена авторизации для iiko API."""
    if not api_key or not str(api_key).strip():
        raise ValueError("iiko api_key is empty")
    url = 'https://api-ru.iiko.services/api/1/access_token'
    data = {'apiLogin': api_key}
    response = requests.post(url, json=data)
    response.raise_for_status()
    data_response = response.json()
    if 'token' not in data_response:
        logger.error("iiko token response missing 'token': %s", data_response)
        raise ValueError("Invalid iiko token response")
    return data_response['token']


def organization(api_key):
    """Получение списка организаций из iiko."""
    url = 'https://api-ru.iiko.services/api/1/organizations'
    headers = {"Authorization": f"Bearer {token(api_key)}"}
    data = {'apiLogin': api_key}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return [org['id'] for org in response.json()['organizations']]
    except Exception as e:
        logger.error(f"Failed to get organizations for api_key {api_key}: {e}")
        raise

def get_order_types(pickup_area=None):
    """Получение типов заказов из iiko с учетом PickupAreas."""
    api_key = get_iiko_api_key(pickup_area)
    if not api_key:
        logger.error("No iiko api_key for get_order_types")
        return None
    url = "https://api-ru.iiko.services/api/1/deliveries/order_types"
    headers = {"Authorization": f"Bearer {token(api_key)}"}
    orgs = organization(api_key)
    
    data = {"organizationIds": orgs}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        # print(response.json())
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get order types for api_key {api_key}: {e}")
        raise

def get_terminal_groups(pickup_area=None):
    """Получение ID группы терминалов из iiko с учетом PickupAreas."""
    api_key = get_iiko_api_key(pickup_area)
    if not api_key:
        logger.error("No iiko api_key for get_terminal_groups")
        return None
    url = 'https://api-ru.iiko.services/api/1/terminal_groups'
    headers = {"Authorization": f"Bearer {token(api_key)}"}
    orgs = organization(api_key)
    
    data = {"organizationIds": orgs}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        terminal_groups = response.json()['terminalGroups']

        return terminal_groups[0]['items'][0]['id']
        
        
    except Exception as e:
        logger.error(f"Failed to get terminal groups for api_key {api_key}: {e}")
        raise



def get_tables(pickup_area, table_num):
    if not pickup_area:
        return None
    api_key = get_iiko_api_key(pickup_area)
    if not api_key:
        logger.error("No iiko api_key for get_tables")
        return None
    terminal_group = pickup_area.terminal_group

    url = 'https://api-ru.iiko.services/api/1/reserve/available_restaurant_sections'
    headers = {"Authorization": f"Bearer {token(api_key)}"}

    data = {
        "terminalGroupIds": [
            terminal_group
        ]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Получаем JSON-ответ
        response_data = response.json()
        
        # Ищем стол с указанным номером
        for section in response_data.get('restaurantSections', []):
            for table in section.get('tables', []):
                if table.get('number') == table_num:
                    # print(table.get('posId'))
                    return table.get('posId')
        
        # Если стол не найден, возвращаем None
        logger.warning(f"Table number {table_num} not found")
        return None

    except Exception as e:
        logger.error(f"Failed to get tables: {e}")
        return None

# pickup_area=PickupAreas.objects.get(terminal_group="24cdd250-8686-4b95-a1d0-23dc45612fc8")
# get_tables(pickup_area, 1)


def extract_digits_from_end(input_string):
    """Извлечение цифр из конца строки."""
    if not input_string:
        return None
    match = re.search(r'\d+$', input_string)
    return match.group() if match else None

def get_menu(api_key):
    """Получение меню из iiko."""
    url = 'https://api-ru.iiko.services/api/2/menu'
    headers = {"Authorization": f"Bearer {token(api_key)}"}
    response = requests.post(url, headers=headers)
    # print(response.json())
    
    return response.json()



def generate_unique_slug(base_slug, model_class, exclude_id=None):
    """Генерация уникального slug с добавлением числового суффикса при необходимости."""
    slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=slug).exclude(id=exclude_id).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


def sync_products(pickup_area=None):
    """Синхронизация товаров из iiko для конкретной точки или глобально."""
    api_key = get_iiko_api_key(pickup_area)
    if not api_key:
        logger.error("No iiko api_key for sync_products")
        return
    if pickup_area:
        show_in_site = pickup_area.show_in_site
        related_pickup_areas = PickupAreas.objects.filter(api_key=api_key)
    else:
        show_in_site = True
        related_pickup_areas = []

    # Получаем меню
    menu_data = get_menu(api_key)

    menu_id = menu_data['externalMenus'][0]['id']
    try:
        price_category_id = menu_data.get('priceCategories', [{}])[0].get('id')
    except:
        price_category_id = None

    # Запрос детального меню
    url_menu_id = 'https://api-ru.iiko.services/api/2/menu/by_id'
    headers = {"Authorization": f"Bearer {token(api_key)}"}
    data = {
        "externalMenuId": menu_id,
        "organizationIds": organization(api_key),
    }
    if price_category_id:
        data['priceCategoryId'] = price_category_id

    menu_response = requests.post(url_menu_id, json=data, headers=headers)
    menu_json = menu_response.json()


    # Сохранение меню для отладки
    with open(f'menu_{api_key}.json', 'w', encoding='utf-8') as f:
        json.dump(menu_json, f, ensure_ascii=False, indent=4)

    # Собираем все product_id из меню
    menu_product_ids = set()
    for cat in menu_json['itemCategories']:
        for product in cat['items']:
            menu_product_ids.add(product['itemId'])


    

    # Получаем существующие товары в базе
    if related_pickup_areas:
        existing_products = Product.objects.filter(pickup_areas__in=related_pickup_areas).exclude(external_id__isnull=True)
    else:
        existing_products = Product.objects.all().exclude(external_id__isnull=True)

    # Удаляем товары, которых нет в меню
    for product in existing_products:
        if product.external_id not in menu_product_ids:
            product.delete()    

    # print(menu_json)

    # Обновляем или создаем товары
    for cat in menu_json['itemCategories']:
        cat_name = cat['name']
        cat_id = cat['id']
        # Генерируем базовый slug
        cat_slug_base = slugify(cat_name)
        # При show_in_site=False добавляем external_id для уникальности
        cat_slug = f"{cat_slug_base}-{cat_id}" if not show_in_site else cat_slug_base
        # Обеспечиваем уникальность slug
        cat_slug = generate_unique_slug(cat_slug, Category)

        if "*" in cat_name:
            continue 
        cat_name = re.sub(r'\d+', '', cat_name)
        cat_name = cat_name.replace('.', '')
        cat_name = cat_name.replace('. ', '')

        cat_exists = Category.objects.filter(pickup_areas__in=related_pickup_areas, name=cat_name).exists()
        if cat_exists:
            cat_query = Category.objects.filter(pickup_areas__in=related_pickup_areas, name=cat_name)
            cat_save = cat_query.first()
        
        else:
            # Проверяем, существует ли категория с таким external_id
            cat_query = Category.objects.filter(external_id=cat_id)
            if related_pickup_areas:
                # Фильтруем по одной из related_pickup_areas, чтобы найти существующую категорию
                cat_query = cat_query.filter(pickup_areas__in=related_pickup_areas)

            if cat_query.exists():
                cat_save = cat_query.first()
                cat_save.name = cat_name
                cat_save.slug = generate_unique_slug(cat_slug, Category, exclude_id=cat_save.id)
                cat_save.show_in_site = show_in_site
                cat_save.save()
                # Обновляем связи с PickupAreas
                if related_pickup_areas:
                    for area in related_pickup_areas:
                        if area not in cat_save.pickup_areas.all():
                            cat_save.pickup_areas.add(area)
            else:
                cat_save = Category.objects.create(
                    external_id=cat_id,
                    name=cat_name,
                    slug=cat_slug,
                    top=False,
                    show_in_site=show_in_site
                )
                # Привязываем ко всем related_pickup_areas
                if related_pickup_areas:
                    cat_save.pickup_areas.set(related_pickup_areas)



        for product in cat['items']:
            product_id = product['itemId']
            product_name = product['name']
            product_description = product['description']
            item_options = product['itemSizes']

            try:
                price = Decimal(item_options[0]['prices'][0]['price']) or Decimal('0')
            except (IndexError, KeyError, TypeError):
                # print(f"Skipping product {product_name} due to missing data.")
                continue

            try:
                weight = int(item_options[0].get('portionWeightGrams', 0)) or None
            except (IndexError, KeyError, TypeError):
                weight = None
            try:
                image_url = item_options[0].get('buttonImageUrl')
            except (IndexError, KeyError, TypeError):
                image_url = None


            # Генерируем slug
            product_slug = generate_unique_slug(slugify(product_name), Product)


            product_name_exists = Product.objects.filter(name=product_name, pickup_areas__in=related_pickup_areas)

            # Проверяем существующий товар
            product_query = Product.objects.filter(external_id=product_id)
            if related_pickup_areas:
                product_query = product_query.filter(pickup_areas__in=related_pickup_areas)

            if product_query.exists():
                product_save = product_query.first()
                product_save.parent = cat_save
                product_save.name = product_name
                product_save.price = price
                product_save.short_description = product_description
                product_save.weight = weight
                if related_pickup_areas:
                    product_save.pickup_areas.set(related_pickup_areas)

                product_save.save()
            else:
                product_save = Product.objects.create(
                    parent=cat_save,
                    external_id=product_id,
                    name=product_name,
                    slug=product_slug,
                    price=price,
                    short_description=product_description,
                    iiko_type=product['orderItemType'],
                    weight=weight,
                )
                if related_pickup_areas:
                    product_save.pickup_areas.set(related_pickup_areas)

            # Загрузка изображения
            if image_url:
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_name = image_url.split('/')[-1]
                        product_save.thumb.save(image_name, ContentFile(response.content), save=True)
                except Exception as e:
                    logger.error(f"Failed to load image for {product_name}: {e}")

    return {"status": "success", "message": "Products synchronized successfully"}


# sync_products(pickup_area=PickupAreas.objects.get(name="Посёлок Мещерино, 6"))



def load_menu(clean_categories=False, clean_products=False, pickup_area=None):

    clean_categories = True
    clean_products = True
    # Category.objects.all().delete()

    """Синхронизация меню из iiko с учетом PickupAreas."""
    api_key = get_iiko_api_key(pickup_area)
    if not api_key:
        logger.error("No iiko api_key for load_menu")
        return
    if pickup_area:
        show_in_site = pickup_area.show_in_site
        related_pickup_areas = PickupAreas.objects.filter(api_key=api_key)
    else:
        show_in_site = True
        related_pickup_areas = []

    area_id = str(pickup_area.id) if pickup_area else 'global'

    # Category.objects.all().delete()

    # Очистка данных, если требуется
    if clean_products:
        if related_pickup_areas:
            Product.objects.filter(pickup_areas__in=related_pickup_areas).exclude(external_id__isnull=True).delete()
        else:
            Product.objects.all().exclude(external_id__isnull=True).delete()
    if clean_categories:
        
        if related_pickup_areas:
            Category.objects.filter(pickup_areas__in=related_pickup_areas).delete()
        else:
            Category.objects.all().delete()

    # Получаем меню
    menu_data = get_menu(api_key)
    menu_id = menu_data['externalMenus'][0]['id']
    try:
        price_category_id = menu_data.get('priceCategories', [{}])[0].get('id')
    except:
        price_category_id = None

    # Запрос детального меню
    url_menu_id = 'https://api-ru.iiko.services/api/2/menu/by_id'
    headers = {"Authorization": f"Bearer {token(api_key)}"}
    orgs = organization(api_key)
    data = {
        "externalMenuId": menu_id,
        "organizationIds": orgs,
    }
    if price_category_id:
        data['priceCategoryId'] = price_category_id

    menu_response = requests.post(url_menu_id, json=data, headers=headers)
    menu_json = menu_response.json()

    # Сохранение меню для отладки
    with open(f'menu_{area_id}.json', 'w', encoding='utf-8') as f:
        json.dump(menu_json, f, ensure_ascii=False, indent=4)

    # Обработка категорий
    for cat in menu_json['itemCategories']:
        cat_name = cat['name']
        cat_id = cat['id']
        # Генерируем базовый slug
        cat_slug_base = slugify(cat_name)
        # При show_in_site=False добавляем external_id для уникальности
        cat_slug = f"{cat_slug_base}-{cat_id}" if not show_in_site else cat_slug_base
        # Обеспечиваем уникальность slug
        cat_slug = generate_unique_slug(cat_slug, Category)

        if "*" in cat_name:
            continue 
        # cat_name = re.sub(r'\d+', '', cat_name)
        # cat_name = cat_name.replace('.', '')
        # cat_name = cat_name.replace('. ', '')

        cat_exists = Category.objects.filter(pickup_areas__in=related_pickup_areas, name=cat_name).exists()
        if cat_exists:
            
            cat_query = Category.objects.filter(pickup_areas__in=related_pickup_areas, name=cat_name)
            cat_save = cat_query.first()

        else:
            # Проверяем, существует ли категория с таким external_id
            cat_query = Category.objects.filter(external_id=cat_id)

            try:
                from shop.models import CategorySetup
            except ImportError:
                CategorySetup = None

            cat_setup = None
            if CategorySetup is not None:
                cat_setup = CategorySetup.objects.filter(category_external_id=cat_id).first()
                if not cat_setup:
                    cat_setup, _ = CategorySetup.objects.get_or_create(category_external_id=cat_id)

            slug = cat_setup.slug if cat_setup else generate_unique_slug(cat_slug, Category)
            home = cat_setup.home if cat_setup else None


            if related_pickup_areas:
                # Фильтруем по одной из related_pickup_areas, чтобы найти существующую категорию
                cat_query = cat_query.filter(pickup_areas__in=related_pickup_areas)

            if cat_query.exists():

                
                cat_save = cat_query.first()
                cat_save.name = cat_name
                cat_save.slug = slug
                cat_save.show_in_site = show_in_site
                cat_save.top = show_in_site
                cat_save.home = home
                cat_save.image = cat_setup.image if cat_setup else None
                cat_save.image_qr = cat_setup.image_qr if cat_setup else None
                cat_save.resize = cat_setup.resize if cat_setup else None
                cat_save.font_color = cat_setup.font_color if cat_setup else None
                cat_save.bg_color = cat_setup.bg_color if cat_setup else None
                cat_save.opacity = cat_setup.opacity if cat_setup else None
                cat_save.sort_order = cat_setup.sort_order if cat_setup else None


                cat_save.save()
                # Обновляем связи с PickupAreas
                if related_pickup_areas:
                    for area in related_pickup_areas:
                        if area not in cat_save.pickup_areas.all():
                            cat_save.pickup_areas.add(area)
            else:
                cat_save = Category.objects.create(
                    external_id=cat_id,
                    name=cat_name,
                    slug=slug,
                    show_in_site=show_in_site,
                    top = show_in_site,
                    home = home,
                    image = cat_setup.image if cat_setup else None,
                    image_qr = cat_setup.image_qr if cat_setup else None,
                    resize = cat_setup.resize if cat_setup else None,
                    font_color = cat_setup.font_color if cat_setup else None,
                    bg_color = cat_setup.bg_color if cat_setup else None,
                    opacity = cat_setup.opacity if cat_setup else None,
                    sort_order = cat_setup.sort_order if cat_setup else None
                )
                # Привязываем ко всем related_pickup_areas
                if related_pickup_areas:
                    cat_save.pickup_areas.set(related_pickup_areas)

        # Обработка товаров
        for idx, product in enumerate(cat['items']):
            product_name = product['name']
            product_id = product['itemId']
            product_description = product['description']
            item_options = product['itemSizes']

            try:
                from shop.models import ProductSetup
            except ImportError:
                ProductSetup = None

            product_setup = None
            if ProductSetup is not None:
                product_setup = ProductSetup.objects.filter(product_external_id=product_id).first()
                if not product_setup:
                    product_setup, _ = ProductSetup.objects.get_or_create(product_external_id=product_id)



            try:
                price = Decimal(item_options[0]['prices'][0]['price']) or Decimal('0')
            except (IndexError, KeyError, TypeError):
                # print(f"Skipping product {product_name} due to missing data.")
                continue

            try:
                weight = int(item_options[0].get('portionWeightGrams', 0)) or None
            except (IndexError, KeyError, TypeError):
                weight = None
            try:
                image_url = item_options[0].get('buttonImageUrl')
            except (IndexError, KeyError, TypeError):
                image_url = None
                

            # Генерируем базовый slug
            product_slug_base = slugify(product_name)
            # При show_in_site=False добавляем external_id для уникальности
            product_slug = f"{product_slug_base}-{product_id}" if not show_in_site else product_slug_base
            # Обеспечиваем уникальность slug
            product_slug = generate_unique_slug(product_slug, Product)

            # Проверяем, существует ли продукт с таким external_id
            product_query = Product.objects.filter(external_id=product_id)
            if related_pickup_areas:
                # Фильтруем по одной из related_pickup_areas
                product_query = product_query.filter(pickup_areas__in=related_pickup_areas)

            if product_query.exists():
                product_save = product_query.first()
                product_save.name = product_name
                product_save.slug = product_setup.slug if product_setup else generate_unique_slug(product_slug, Product, exclude_id=product_save.id)
                product_save.price = price
                product_save.short_description = product_description
                product_save.weight = weight
                product_save.show_in_site = show_in_site

                product_save.new = product_setup.new if product_setup else None
                product_save.bestseller = product_setup.bestseller if product_setup else None
                product_save.related = product_setup.related if product_setup else None
                product_save.all_cats = product_setup.all_cats if product_setup else None
                product_save.free = product_setup.free if product_setup else None
                product_save.minimum = product_setup.minimum if product_setup else None
                product_save.in_cart = product_setup.in_cart if product_setup else None
                
            

                product_save.save()
                if product_setup is not None:
                    product_setup.product_id = product_save.id
                    product_setup.save()
                # Обновляем связи с PickupAreas
                if related_pickup_areas:
                    for area in related_pickup_areas:
                        if area not in product_save.pickup_areas.all():
                            product_save.pickup_areas.add(area)
            else:
                product_save = Product.objects.create(
                    external_id=product_id,
                    name=product_name,
                    slug=product_slug,
                    price=price,
                    parent=cat_save,
                    short_description=product_description,
                    iiko_type=product['orderItemType'],
                    weight=weight,
                    show_in_site=show_in_site,
                    new = product_setup.new if product_setup else None,
                    bestseller = product_setup.bestseller if product_setup else None,
                    related = product_setup.related if product_setup else None,
                    all_cats = product_setup.all_cats if product_setup else None,
                    free = product_setup.free if product_setup else None,
                    minimum = product_setup.minimum if product_setup else None,
                    in_cart = product_setup.in_cart if product_setup else None
                )
                # Привязываем ко всем related_pickup_areas
                if related_pickup_areas:
                    product_save.pickup_areas.set(related_pickup_areas)

                product_setup.product_id = product_save.id
                product_setup.save()

            # Загрузка изображения
            if image_url:
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_name = image_url.split('/')[-1]
                        product_save.thumb.save(image_name, ContentFile(response.content), save=True)
                except Exception as e:
                    logger.error(f"Failed to load image for {product_name}: {e}")

            # Обработка опций (размеры)
            if len(item_options) > 1:
                product_save.options.all().delete()
                option_type, _ = OptionType.objects.get_or_create(option_class='select', name='Размер')

                for option in item_options:
                    option_name = option.get('sizeName')
                    option_price = Decimal(option['prices'][0]['price']) - price if option['prices'][0]['price'] != price else 0
                    option_weight = option.get('portionWeightGrams')
                    option_image_url = option.get('buttonImageUrl')

                    option_save = ProductOption.objects.create(
                        parent=product_save,
                        option_value=option_name,
                        option_price=option_price,
                        option_weight=option_weight,
                        type=option_type
                    )

                    if option_image_url:
                        try:
                            response = requests.get(option_image_url)
                            if response.status_code == 200:
                                image_name = option_image_url.split('/')[-1]
                                op_image = OptionImage.objects.create(parent=option_save)
                                op_image.src.save(image_name, ContentFile(response.content), save=True)
                        except Exception as e:
                            logger.error(f"Failed to load option image for {option_name}: {e}")

# load_menu(True, True, None)






def create_iiko_order(order, attempt=1, pickup_area=None):
    """Создание заказа в iiko с учетом PickupAreas."""
    try:
        api_key = get_iiko_api_key(pickup_area)
        if not api_key:
            logger.error("No iiko integration found")
            return

        if attempt > 12:
            logger.error(f"Max attempts reached for order {order.id}. Giving up.")
            return

        url = 'https://api-ru.iiko.services/api/1/deliveries/create'
        headers = {"Authorization": f"Bearer {token(api_key)}"}

        integration = get_iiko_integration()
        if pickup_area and getattr(pickup_area, 'organization_id', None):
            org_id = pickup_area.organization_id
        elif integration:
            org_id = getattr(integration, 'organization_id', None)
        else:
            org_id = None
        if not org_id:
            logger.error("No iiko organization_id configured")
            return

        # Формируем элементы заказа
        items = [
            {
                "productId": item.product.external_id,
                "price": float(item.product.price) if isinstance(item.product.price, Decimal) else item.product.price,
                "type": item.product.iiko_type,
                "amount": item.quantity
            }
            for item in order.items.all()
        ]

        # Генерируем и сохраняем UUID заказа
        order_uuid = str(uuid.uuid4())
        order.external_id = order_uuid
        order.save()

        # Получаем тип заказа
        order_types = get_order_types(pickup_area)
        if not order_types:
            logger.error("Could not get order types from iiko")
            return
        delivery_method_map = {
            "Доставка": "Доставка курьером",
            "Самовывоз": "Доставка самовывоз"
        }
        order_type_id = next(
            (
                item['id']
                for order_type in order_types['orderTypes']
                for item in order_type['items']
                if item['name'] == delivery_method_map.get(order.delivery_method)
            ),
            None
        )
        if not order_type_id:
            logger.error(f"No matching order type found for delivery method {order.delivery_method}")
            return

        # Формируем данные доставки
        delivery_point = None
        if order.delivery_method == "Доставка":
            delivery_point = {
                "address": {
                    "street": {"name": order.address or ""},
                    "house": extract_digits_from_end(order.address) or "",
                    "flat": order.flat or "",
                    "entrance": order.entrance or "",
                    "floor": order.floor or "",
                    "type": "legacy",
                },
            }

        # Формируем данные заказа
        data = {
            "organizationId": org_id,
            "order": {
                "id": order_uuid,
                "customer": {
                    "name": order.name or "Unknown",
                    "phone": order.phone or "+79999999999",
                    "type": "regular"
                },
                "phone": order.phone or "",
                "fulfillmentType": "delivery",
                "deliveryFee": float(order.delivery_price) if order.delivery_price else 0.0,
                "textOrderContent": "Заказ: " + ", ".join([f"{item.product.name} x{item.quantity}" for item in order.items.all()]),
                "items": items,
                "orderTypeId": order_type_id,
                "comment": f"{order.time} / {order.order_conmment or ''}",
            }
        }

        if pickup_area and getattr(pickup_area, 'terminal_group', None):
            data['terminalGroupId'] = pickup_area.terminal_group
        elif integration and getattr(integration, 'terminal_group', None):
            data['terminalGroupId'] = integration.terminal_group
        else:
            logger.warning("No iiko terminal_group configured")

        # Добавляем точку доставки, если это доставка
        if delivery_point:
            data['order']['deliveryPoint'] = delivery_point

        # Отправляем запрос
        response = requests.post(url, json=data, headers=headers)


        # print(response.json())

        if response.status_code == 200:
            logger.info(f"Order {order.id} created successfully in iiko")
            threading.Thread(target=background_order_status_check, args=(order, order_uuid, attempt, pickup_area)).start()
        else:
            logger.error(f"Failed to create order {order.id}: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"Error creating order {order.id}: {e}")






def create_iiko_table(order, attempt=1, pickup_area=None):
    """Создание заказа в iiko с учетом PickupAreas."""
    try:
        api_key = get_iiko_api_key(pickup_area)
        if not api_key:
            logger.error("No iiko integration found")
            return

        if attempt > 12:
            logger.error(f"Max attempts reached for order {order.id}. Giving up.")
            return

        url = 'https://api-ru.iiko.services/api/1/order/create'
        headers = {"Authorization": f"Bearer {token(api_key)}"}

        integration = get_iiko_integration()
        if pickup_area and getattr(pickup_area, 'organization_id', None):
            org_id = pickup_area.organization_id
        elif integration:
            org_id = getattr(integration, 'organization_id', None)
        else:
            org_id = None
        if not org_id:
            logger.error("No iiko organization_id configured")
            return

        # Формируем элементы заказа
        items = [
            {
                "productId": item.product.external_id,
                "price": float(item.product.price) if isinstance(item.product.price, Decimal) else item.product.price,
                "type": item.product.iiko_type,
                "amount": item.quantity
            }
            for item in order.items.all()
        ]

        # Генерируем и сохраняем UUID заказа
        order_uuid = str(uuid.uuid4())
        order.external_id = order_uuid
        order.save()

        # Получаем тип заказа
        order_types = get_order_types(pickup_area)
        if not order_types:
            logger.error("Could not get order types from iiko")
            return
        order_type_id = next(
            (
                item['id']
                for order_type in order_types['orderTypes']
                for item in order_type['items']
                if item['name'] == 'Обычный заказ'
            ),
            None
        )
        if not order_type_id:
            logger.error(f"No matching order type found for delivery method {order.delivery_method}")
            return
        
        # Формируем данные заказа
        
        data = {
            "organizationId": org_id,
            "order": {
                "id": order_uuid,
                "items": items,
                "orderTypeId": order_type_id,
                # "tableIds": [
                #     get_tables(pickup_area, int(order.table_object.name))
                # ],
                "comment": f"{order.time} / {order.order_conmment or ''} / Заказ для стола {order.table_object.name}",
            }
        }

        if pickup_area and getattr(pickup_area, 'terminal_group', None):
            data['terminalGroupId'] = pickup_area.terminal_group
        elif integration and getattr(integration, 'terminal_group', None):
            data['terminalGroupId'] = integration.terminal_group
        else:
            logger.warning("No iiko terminal_group configured")

        # Отправляем запрос
        response = requests.post(url, json=data, headers=headers)

        # print(response.json())

        if response.status_code == 200:
            logger.info(f"Order {order.id} created successfully in iiko")
            threading.Thread(target=background_order_table_status_check, args=(order, order_uuid, attempt, pickup_area)).start()
        else:
            logger.error(f"Failed to create order {order.id}: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"Error creating order {order.id}: {e}")


def check_order_status(order_id, pickup_area=None):
    """Проверка статуса заказа в iiko."""
    api_key = get_iiko_api_key(pickup_area)
    if not api_key:
        logger.error("No iiko api_key for check_order_status")
        return None
    integration = get_iiko_integration()
    if pickup_area and getattr(pickup_area, 'organization_id', None):
        org_id = pickup_area.organization_id
    elif integration:
        org_id = getattr(integration, 'organization_id', None)
    else:
        org_id = None
    if not org_id:
        logger.error("No iiko organization_id for check_order_status")
        return None
    url = 'https://api-ru.iiko.services/api/1/deliveries/by_id'
    headers = {"Authorization": f"Bearer {token(api_key)}"}

    data = {
        "organizationId": org_id,
        "orderIds": [order_id]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        # print(response.json())
        return response.json()
    except Exception as e:
        logger.error(f"Failed to check order status for order {order_id}: {e}")
        return None

# check_order_status("b39b1946-ffbe-43a4-bacb-b815f05ca1be")


def check_order_table_status(order_id, pickup_area=None):
    """Проверка статуса заказа в iiko."""
    api_key = get_iiko_api_key(pickup_area)
    if not api_key:
        logger.error("No iiko api_key for check_order_table_status")
        return None
    integration = get_iiko_integration()
    if pickup_area and getattr(pickup_area, 'organization_id', None):
        org_id = pickup_area.organization_id
    elif integration:
        org_id = getattr(integration, 'organization_id', None)
    else:
        org_id = None
    if not org_id:
        logger.error("No iiko organization_id for check_order_table_status")
        return None
    url = 'https://api-ru.iiko.services/api/1/order/by_id'
    headers = {"Authorization": f"Bearer {token(api_key)}"}

    data = {
        "organizationIds": [org_id],
        "orderIds": [order_id]
    }

    # print(data)
    # print(headers)

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        # print(response.json())
        return response.json()
    except Exception as e:
        logger.error(f"Failed to check order status for order {order_id}: {e}")
        return None
    


# check_order_status("", pickup_area=PickupAreas.objects.get(name="Посёлок Мещерино, 6"))

# /api/1/reserve/available_restaurant_sections








def background_order_table_status_check(order, order_id, attempt, pickup_area=None):
    """Фоновая проверка статуса заказа."""
    max_duration = 3600  # 1 час
    delay = 30  # 30 секунд
    start_time = time.time()

    while time.time() - start_time < max_duration:
        status_response = check_order_table_status(order_id, pickup_area)
        if status_response and 'orders' in status_response and any(order['id'] == order_id for order in status_response['orders']):
            logger.info(f"Order {order_id} has been processed")

            return
        time.sleep(delay)

    logger.warning(f"Order {order_id} status check timed out. Retrying (Attempt {attempt + 1})")
    create_iiko_table(order, attempt + 1, pickup_area)



def background_order_status_check(order, order_id, attempt, pickup_area=None):
    """Фоновая проверка статуса заказа."""
    max_duration = 3600  # 1 час
    delay = 30  # 30 секунд
    start_time = time.time()

    while time.time() - start_time < max_duration:
        status_response = check_order_status(order_id, pickup_area)
        if status_response and 'orders' in status_response and any(order['id'] == order_id for order in status_response['orders']):
            logger.info(f"Order {order_id} has been processed")

            # telegram_bot = '5953442472:AAHsgzGdcVrnuJnb0FnDWJ4nrPdDT59YNOE'
            # telegram_group = '-1002079435900'
            # send_message(telegram_bot, telegram_group, f'Номер заказа в iiko: {order_id}')
            
            return
        time.sleep(delay)

    logger.warning(f"Order {order_id} status check timed out. Retrying (Attempt {attempt + 1})")
    create_iiko_order(order, attempt + 1, pickup_area)





# threading.Thread(target=background_order_status_check, args=(Order.objects.get(id=641), "5ea54446-b2dc-453f-8c4a-d9fb09b591f6", 1)).start()
# pickup_area=PickupAreas.objects.get(terminal_group="Чайхана Мадина Мещерино")
# create_iiko_order(Order.objects.get(id=672), pickup_area=pickup_area)
