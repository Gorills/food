from .models import PaymentSet

def cart_active(request):
    try:
     
        cart_active = PaymentSet.objects.get().status
    except:

        cart_active = False

    return {'cart_active': cart_active}


