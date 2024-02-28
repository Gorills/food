
from .models import Delivery


def delivery(request):
    try:
        delivery_object = Delivery.objects.get()
        
    except:
        delivery_object = None
    return {'delivery': delivery_object}