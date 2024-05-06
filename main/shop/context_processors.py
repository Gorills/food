from .models import Category, Product, ShopSetup, PickupAreas, PayMethod, PickupAreas, Combo

def categorys(request):
    return {'categorys': Category.objects.filter(status=True).order_by('sort_order')}



def categorys_top(request):
    return {'categorys_top': Category.objects.filter(status=True, top=True).order_by('sort_order')}

def combos(request):
    return {'combos': Combo.objects.all()}


# Показывать описания под товарами
def shop_setup(request):
    try:
        return {'shop_setup': ShopSetup.objects.get()}
    except:
        return {'shop_setup': ''}


def pickup_areas(request):
    try:
        return {'pickup_areas': PickupAreas.objects.all()}
    except:
        return {'pickup_areas': ''}


def pay_method(request):
    try:
        return {'pay_method': PayMethod.objects.all()}
    except:
        return {'pay_method': ''}
    


def pickup_address(request):
    try:
        return {'pickup_address': PickupAreas.objects.filter(show_to_contacts=True)}
    except:
        return {'pickup_address': None}
    


def cart_products(request):

    return {'cart_products': Product.objects.filter(in_cart=True, status=True)}