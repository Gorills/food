from .models import Category, ShopSetup

def categorys(request):
    return {'categorys': Category.objects.filter(parent=None, status=True).order_by('sort_order')}


# Показывать описания под товарами
def shop_setup(request):
    try:
        return {'shop_setup': ShopSetup.objects.get()}
    except:
        return {'shop_setup': ''}