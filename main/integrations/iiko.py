import requests

# Create your views here.

from .models import Integrations

api_key = Integrations.objects.get(name='iiko').api_key



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

# organization()
from pytils.translit import slugify
from django.core.files.base import ContentFile
from shop.models import Category, OptionImage, OptionType, Product, ProductOption
import json
def load_menu(clean):

    if clean:
        categories = Category.objects.all()
        categories.delete()


    url = 'https://api-ru.iiko.services/api/2/menu'
    

    headers = {"Authorization": f"Bearer {token()}"}

    response = requests.post(url, headers=headers)
    menu = response.json()['externalMenus'][0]['id']

    

    url_menu_id = 'https://api-ru.iiko.services/api/2/menu/by_id'

    orgs = organization()

    data = {
        "externalMenuId": str(menu),
        "organizationIds": orgs,
    }

    menu_response = requests.post(url_menu_id, json=data, headers=headers)

    # with open(f'menu.json', 'w') as f:
    #     json.dump(menu_response.json(), f)

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
                product_save.type = product['orderItemType']
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
                        type=product['orderItemType'],
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
                        type=product['orderItemType']
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

                    print(option_id, option_name, option_price, option_weight, option_image)
        i += 1
        
            


# load_menu()