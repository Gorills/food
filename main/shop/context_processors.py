from .models import Category, ShopSetup, PickupAreas

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
        return {'shop_setup': ''}