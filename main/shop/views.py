from django.shortcuts import get_object_or_404, render
from .models import Category, Product, ProductChar, ProductOption, ShopSetup, OptionType
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from cart.cart import Cart
import os
from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'sushi'


from .sort import func_sort
# Create your views here.


def catalog(request):
    # cart = Cart(request)
    # cart.clear()
    sort = request.GET.getlist('sort')
    limit = request.GET.getlist('limit')
    page_number = request.GET.get('page')
    

    

    try:

        min_filter = Product.objects.all().order_by('price').first().price
        max_filter = Product.objects.all().order_by('-price').first().price
    except:
        
        min_filter = 0
        max_filter = 0

    
    try:
        min_price = request.GET['min_price']
    except:
        min_price = min_filter
    try:
        max_price = request.GET['max_price']
    except:
        max_price = max_filter


    product_list = Product.objects.filter(status=True, related=False, price__gte=min_price, price__lte=max_price).exclude(stock=0).order_by(*sort)
    # product_list = Product.objects.filter(status=True, price__gte=min_price, price__lte=max_price).order_by(*sort)

    


    if limit:
        paginator = Paginator(product_list, *limit)
    else:
        paginator = Paginator(product_list, 16)


    page_number = request.GET.get('page')

    products = paginator.get_page(page_number)

    # products = func_sort(*sort, limit)

    char_filtres = ProductChar.objects.filter(parent__in=product_list).distinct('char_value')


    context = {
        'products': products,
        'char_filtres': char_filtres,
        
        'shop_setup': ShopSetup.objects.get(),

        'sort': sort,
        'limit': limit,

        'min_filter': min_filter,
        'max_filter': max_filter,
        'min_price': min_price,
        'max_price': max_price
    }


    return render(request, 'shop/catalog.html', context)




def category_detail(request, slug):
    sort = request.GET.getlist('sort')
    limit = request.GET.getlist('limit')
    page_number = request.GET.get('page')

    category = get_object_or_404(Category, slug=slug)
    
    if category.status == True:
        try:

            products_list = Product.objects.filter(status=True, stock__gt=0, related=False, parent=category)
            
            min_filter = products_list.order_by('price').first().price
            max_filter = products_list.order_by('-price').first().price
        except:
            products_list = []
            
            min_filter = 0
            max_filter = 0
            
        try:
            min_price = request.GET['min_price']
        except:
            min_price = min_filter
        try:
            max_price = request.GET['max_price']
        except:
            max_price = max_filter


        products_all = Product.objects.filter(status=True, parent=category, price__gte=min_price, price__lte=max_price).exclude(stock=0).order_by(*sort)

        if limit:
            paginator = Paginator(products_all, *limit)
        else:
            paginator = Paginator(products_all, 600)


        page_number = request.GET.get('page')

        products = paginator.get_page(page_number)


        context = {
            
            'category': category,
            'products': products,
            'category_children': category.children.all(),
            'shop_setup': ShopSetup.objects.get(),
            'sort': sort,
            'limit': limit,
            'min_filter': min_filter,
            'max_filter': max_filter,
            'min_price': min_price,
            'max_price': max_price
        }


        return render(request, 'shop/category_detail.html', context)
    else:

        return render(request, '404.html', status=404)


from itertools import groupby
def product_detail(request, parent, slug):
    product = get_object_or_404(Product, slug=slug, status=True)

    product_options = ProductOption.objects.filter(parent=product)

    products_op = []
    for pr in product_options:
        products_op.append(pr.id)

   

    types = OptionType.objects.filter(t_options__in=product_options)

    options_type = []
    for t in types:
        options_type.append(t.id)
    
    new_x = [el for el, _ in groupby(options_type)]

    filter_types = OptionType.objects.filter(id__in=new_x)

    
    similars = Product.objects.order_by("?").filter(parent_id=product.parent.id, related=False)[:8]
    
    try:
        option_second = ProductOption.objects.filter(parent=product)[1]
    except:
        option_second = []

    context = {
        'product': product,
        'cart_product_form': CartAddProductForm(),
        'shop_setup': ShopSetup.objects.get(),
        'product_options': product_options,
        'similars':similars, 
        'products_op': products_op,
        'types': filter_types,
        'option_second': option_second
        }

    return render(request, 'shop/product_detail.html', context)