import datetime
from django.shortcuts import render

from subdomains.utilites import get_protocol

from shop.models import Category, Product

# Create your views here.


def feed(request):
   
    products = Product.objects.filter(status=True)

    cat = Category.objects.filter(status=True)
    
    
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M")

    context = {
        'cats': cat, 
        'products': products,
        
        'formatted_date': formatted_date
    }

    return render(request, 'global/feed.html', context, content_type="application/xml")

