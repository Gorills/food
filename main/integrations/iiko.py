from decimal import Decimal
import requests
import uuid

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

    # with open('menu.json', 'w', encoding='utf-8') as f:
    #     json.dump(menu_response.json(), f, ensure_ascii=False, indent=4)

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
            price = item_options[0]['prices'][0]['price']
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
                print(image)
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

                    print(option_id, option_name, option_price, option_weight, option_image)
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






def get_terminal_groups():

    url = 'https://api-ru.iiko.services/api/1/terminal_groups'

    headers = {"Authorization": f"Bearer {token()}"}

    orgs = organization()

    data = {
        "organizationIds": orgs
    }

    response = requests.post(url, json=data, headers=headers)


    

    return response.json()['terminalGroups'][0]['items'][0]['id']




# Пример функции для создания нового заказа
def create_iiko_order(order):
    url = 'https://api-ru.iiko.services/api/1/order/create'
    headers = {"Authorization": f"Bearer {token()}"}
    orgs = organization()[0]
    terminal_group = get_terminal_groups()

    items = []

    for item in order.items.all():
        items.append({
            "productId": item.product.external_id,
            "price": float(item.product.price) if isinstance(item.product.price, Decimal) else item.product.price,
            "type": item.product.iiko_type,
            "amount": item.quantity
        })

    # Генерация UUID для order.id
    order_uuid = str(uuid.uuid4())
    order.external_id = order_uuid
    order.save()

    items = []

    order_types = get_order_types()

    delivery_method_map = {
        "Доставка": "Доставка курьером",
        "Самовывоз": "Доставка самовывоз"
    }

    # Поиск подходящего метода по названию
    for order_type in order_types['orderTypes']:
        for item in order_type['items']:
            if item['name'] == delivery_method_map.get(order.delivery_method):
                orderTypeId = item['id']
                break
        if orderTypeId:
            orderTypeId = None
            break

    for item in order.items.all():
        items.append({
            "productId": item.product.external_id,
            "price": float(item.product.price) if isinstance(item.product.price, Decimal) else item.product.price,
            "type": item.product.iiko_type,
            "amount": item.quantity
        })

    data = {
        "event": "newOrder",
        "organizationId": orgs,
        "terminalGroupId": terminal_group,
        "order": {
            "id": order_uuid,  # Используем сгенерированный GUID
            "customer": {
                "name": order.name,
                "phone": order.phone,
                "type": "regular"
            },
            "phone": order.phone,
            "address": {
                "street": order.address,
                "apartment": order.flat
            },
            "fulfillmentType": "delivery",  # Указываем тип выполнения заказа
            "deliveryFee": float(order.delivery_price) if order.delivery_price else 0.0,  # Стоимость доставки, если она есть
            "textOrderContent": "Заказ: " + ", ".join([f"{item.product.name} x{item.quantity}" for item in order.items.all()]),
            "items": items,
            "notes": order.comment if hasattr(order, 'comment') else ""  # Комментарий к заказу, если есть
        }
    }

    if orderTypeId:
        data['order']['orderTypeId'] = orderTypeId

    print(data)

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Order created successfully")
        print(response.json())
    else:
        print(f"Failed to create order: {response.status_code}")
        print(response.json())







# create_iiko_order(Order.objects.get(id=512))
