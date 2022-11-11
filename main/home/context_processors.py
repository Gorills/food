from .models import Page
from orders.forms import OrderCreateForm

def pages(request):
    return {'pages': Page.objects.filter(status=True)}

def odrer_form(request):
    return {'odrer_form': OrderCreateForm()}


