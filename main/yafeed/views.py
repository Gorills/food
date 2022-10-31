from django.shortcuts import render


from shop.models import Category, Product

# Create your views here.


def feed(request):
   
    products = Product.objects.filter(status=True)[:20]

    cat = Category.objects.filter(status=True)
    

    context = {
        'cats': cat, 
        'products': products
    }

    return render(request, 'yafeed/feed.html', context)