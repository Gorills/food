from decimal import Decimal
import requests
import uuid
import threading
import time
from orders.models import Order

# Create your views here.

from .models import Integrations


from pytils.translit import slugify
from django.core.files.base import ContentFile
from shop.models import Category, OptionImage, OptionType, Product, ProductOption
import json

try:
    api_key = Integrations.objects.get(name='iiko').api_key
except:
    pass




def token():
    url = 'https://api-ru.iiko.services/api/1/access_token'
    data = {
        'apiLogin': api_key
    }
    response = requests.post(url, json=data)

    return response.json()['token']


# token()


def organization():
    url = 'https://api-ru.iiko.services/api/1/organizations'
    headers = {"Authorization": f"Bearer {token()}"}
    data = {
        'apiLogin': api_key
    }
    
    response = requests.post(url, json=data, headers=headers)

    org_list = []

    for org in response.json()['organizations']:
        org_list.append(org['id'])
    
    return org_list


def get_menu():
    url = 'https://api-ru.iiko.services/api/2/menu'
    headers = {"Authorization": f"Bearer {token()}"}
    response = requests.post(url, headers=headers)
    
    return response.json()



# organization()

def load_menu(clean, product_clean):

    headers = {"Authorization": f"Bearer {token()}"}

    if product_clean:
        products = Product.objects.all()
        products.delete()

    if clean:
        categories = Category.objects.all()
        categories.delete()

    get_menu_response = get_menu()

    menu = get_menu_response['externalMenus'][0]['id']

    try:
        priceCategoryId = get_menu_response['priceCategories'][0]['id']
    except:
        priceCategoryId = None

    # print("menu", get_menu_response)
    

    url_menu_id = 'https://api-ru.iiko.services/api/2/menu/by_id'

    orgs = organization()

    data = {
        "externalMenuId": str(menu),
        "organizationIds": orgs,
    }

    if priceCategoryId:
        data['priceCategoryId'] = priceCategoryId


    # print(data)

    menu_response = requests.post(url_menu_id, json=data, headers=headers)

    with open('menu.json', 'w', encoding='utf-8') as f:
        json.dump(menu_response.json(), f, ensure_ascii=False, indent=4)

    for cat in menu_response.json()['itemCategories']:
        cat_name = cat['name']
        cat_slug = slugify(cat_name)
        cat_id = cat['id']

        try:
            cat_save = Category.objects.create(
                external_id=cat_id,
                name=cat_name,
                slug=cat_slug,
                top = True

            )
        except:
            cat_save = Category.objects.get(
                external_id=cat_id
            )
        i = 0
        for product in cat['items']:

            
            product_name = product['name']
            product_slug = slugify(product_name)
            product_id = product['itemId']
            product_description = product['description']

            item_options = product['itemSizes']

            weight = int(item_options[0]['portionWeightGrams'])

            if weight == 0:
                weight = None

            try:
                price = item_options[0]['prices'][0]['price']
            except (IndexError, KeyError, TypeError):
                price = 0

            if price is None:
                print(f"Warning: Skipping product {product_name} due to missing price.")
                continue  # Пропустить продукт без цены

            image = item_options[0]['buttonImageUrl']
            try:
                product_save = Product.objects.get(
                    external_id=product_id
                )
                product_save.weight = weight
                product_save.name = product_name
                product_save.slug = product_slug
                product_save.price = price
                product_save.short_description=product_description
                product_save.iiko_type = product['orderItemType']
                product_save.save()

            except:
                try:
                    product_save = Product.objects.create(
                        external_id=product_id,
                        name=product_name,
                        slug=product_slug, 
                        price=price,
                        parent=cat_save,
                        short_description=product_description,
                        iiko_type=product['orderItemType'],
                        weight=weight
                    )
                except:
                    product_save = Product.objects.create(
                        external_id=product_id,
                        name=product_name,
                        slug=product_slug+str(i), 
                        price=price,
                        parent=cat_save,
                        short_description=product_description,
                        iiko_type=product['orderItemType']
                    )


            try:
                response_pr_img = requests.get(image)
                
                image_name = image.split('/')[-1]
                if response_pr_img.status_code == 200:
                    product_save.thumb.save(image_name, ContentFile(response_pr_img.content), save=True)

            except:
                pass

            
            item_count = len(item_options)

            
            
            if item_count > 1:
                options_old = product_save.options.all()
                options_old.delete()

                for option in item_options:

                
                    option_id = option['sizeId']
                    option_name = option['sizeName']
                    option_price = option['prices'][0]['price']
                    option_weight = option['portionWeightGrams']
                    option_image = option['buttonImageUrl']

                    
                    
                    if option_price == price:
                        option_price = 0

                    else:
                        option_price = int(option_price) - int(price)

                    try:
                        option_type = OptionType.objects.get(option_class='select', name='Размер')
                    except:
                        option_type = OptionType.objects.create(option_class='select', name='Размер')

                    
                    option_save = ProductOption.objects.create(
                        
                        parent=product_save,
                        option_value=option_name,
                        option_price=option_price,
                        option_weight=option_weight,
                        type=option_type

                    )


                    try:
                        op_image = OptionImage.objects.filter(parent=option_save)
                        op_image.delete()

                        response_op_image = requests.get(option_image)
                        op_image_name = image.split('/')[-1]

                        if response_op_image.status_code == 200:

                            op_image = OptionImage.objects.create(
                                parent=option_save,
                                
                            )

                            op_image.src.save(op_image_name, ContentFile(response_op_image.content), save=True)

                    except Exception as e:
                        print(e)

                    
        i += 1
        
            


# load_menu(False)


def get_order_types():

    url = "https://api-ru.iiko.services/api/1/deliveries/order_types"

    headers = {"Authorization": f"Bearer {token()}"}

    orgs = organization()

    data = {
        "organizationIds": orgs
    }

    response = requests.post(url, json=data, headers=headers)

    
    
    return response.json()



# get_order_types()


def get_terminal_groups():

    url = 'https://api-ru.iiko.services/api/1/terminal_groups'

    headers = {"Authorization": f"Bearer {token()}"}

    orgs = organization()

    data = {
        "organizationIds": orgs
    }

    response = requests.post(url, json=data, headers=headers)


    print(response.json())

    return response.json()['terminalGroups'][0]['items'][0]['id']



# get_terminal_groups()


import re

def extract_digits_from_end(input_string):
    match = re.search(r'\d+$', input_string)
    if match:
        return match.group()
    return None




def create_iiko_order(order, attempt=1):

    try:
        integrations = Integrations.objects.get(name='iiko')
    except:
        integrations = None

    if not integrations:
        return

    if attempt > 12:
        print(f"Max attempts reached for order {order.id}. Giving up.")
        return

    url = 'https://api-ru.iiko.services/api/1/deliveries/create'
    headers = {"Authorization": f"Bearer {token()}"}
    orgs = organization()[0]
    
    

    items = [
        {
            "productId": item.product.external_id,
            "price": float(item.product.price) if isinstance(item.product.price, Decimal) else item.product.price,
            "type": item.product.iiko_type,
            "amount": item.quantity
        }
        for item in order.items.all()
    ]

    order_uuid = str(uuid.uuid4())
    order.external_id = order_uuid
    order.save()

    order_types = get_order_types()
    delivery_method_map = {
        "Доставка": "Доставка курьером",
        "Самовывоз": "Доставка самовывоз"
    }

    orderTypeId = next(
        (
            item['id']
            for order_type in order_types['orderTypes']
            for item in order_type['items']
            if item['name'] == delivery_method_map.get(order.delivery_method)
        ),
        None
    )

    deliveryPoint = {
        "address": {
            "street": {"name": order.address},
            "house": extract_digits_from_end(order.address),
            "flat": order.flat,
            "entrance": order.entrance,
            "floor": order.floor,
            "type": "legacy",
        },
    }

    data = {
        "organizationId": orgs,
        "order": {
            "id": order_uuid,
            "customer": {
                "name": order.name,
                "phone": order.phone,
                "type": "regular"
            },
            "phone": order.phone,
            "fulfillmentType": "delivery",
            "deliveryFee": float(order.delivery_price) if order.delivery_price else 0.0,
            "textOrderContent": "Заказ: " + ", ".join([f"{item.product.name} x{item.quantity}" for item in order.items.all()]),
            "items": items,
            "orderTypeId": orderTypeId,
            "comment": f"{order.time} / {order.comment}" if hasattr(order, 'comment') else "",
        }
    }

    try:
        terminal_group = get_terminal_groups()
        data['terminalGroupId'] = terminal_group
    except:
        pass


    if order.delivery_method == "Доставка":
        data['order']['deliveryPoint'] = deliveryPoint

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Order created successfully")
        # print(response.json())
        # Запускаем проверку статуса заказа в отдельном потоке
        threading.Thread(target=background_order_status_check, args=(order, order_uuid, attempt)).start()
    else:
        print(f"Failed to create order: {response.status_code}")
        # print(response.json())


def check_order_status(order_id):
    url = 'https://api-ru.iiko.services/api/1/deliveries/by_id'
    headers = {"Authorization": f"Bearer {token()}"}
    orgs = organization()[0]

    data = {
        "organizationId": orgs,
        "orderIds": [order_id]
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        print(f"Failed to check order status: {response.status_code}")
        # print(response.json())
        return None


def background_order_status_check(order, order_id, attempt):
    max_duration = 3600  # Максимальное время проверки (в секундах)
    delay = 30  # Задержка между проверками (в секундах)
    start_time = time.time()

    while time.time() - start_time < max_duration:
        status_response = check_order_status(order_id)
        if status_response and 'orders' in status_response and any(order['id'] == order_id for order in status_response['orders']):
            print(f"Order {order_id} has been processed.")
            return  # Завершаем проверку при успешном статусе
        time.sleep(delay)

    print(f"Order {order_id} status check timed out. Retrying order creation (Attempt {attempt + 1})...")
    # Повторно отправляем заказ, увеличивая счетчик попыток
    create_iiko_order(order, attempt + 1)



# check_order_status("750a6c1e-4b05-41d7-9aa0-3fc4f887a094")

# threading.Thread(target=background_order_status_check, args=(Order.objects.get(id=578), "8f99da27-4320-402a-83aa-c825d642931d", 1)).start()
# create_iiko_order(Order.objects.get(id=582))
