import datetime
from django.shortcuts import render


from shop.models import Category, Product

# Create your views here.


def feed(request):
   
    products = Product.objects.filter(status=True)

    cat = Category.objects.filter(status=True)
    
    site = 'https://' + str(request.META['HTTP_HOST'])
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M")

    context = {
        'cats': cat, 
        'products': products,
        'site': site,
        'formatted_date': formatted_date
    }

    return render(request, 'global/feed.html', context, content_type="application/xml")

