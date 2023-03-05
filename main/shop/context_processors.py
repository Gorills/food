from .models import Category, ShopSetup, PickupAreas, PayMethod, PickupAreas

def categorys(request):
    return {'categorys': Category.objects.filter(status=True).order_by('sort_order')}


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