from .models import Category, ShopSetup

def categorys(request):
    return {'categorys': Category.objects.filter(parent=None, status=True).order_by('sort_order')}


def view_desc(request):
    try:
        return {'view_desc': ShopSetup.objects.get().show_descrioption}
    except:
        return {'view_desc': ''}