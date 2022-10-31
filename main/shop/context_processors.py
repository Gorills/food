from .models import Category, ShopSetup

def categorys(request):
    return {'categorys': Category.objects.filter(parent=None, status=True).order_by('sort_order')}


