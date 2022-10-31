

from django.core.paginator import Paginator
from .models import Product



def func_sort(*sort, limit):
    
    products = Product.objects.all().order_by(*sort)

    if limit:
        paginator = Paginator(products, *limit)
    else:
        paginator = Paginator(products, 15)

    return products