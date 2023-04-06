from .forms import CallbackForm, OrderCreateForm

def calback_form(request):
    return {'calback_form': CallbackForm()}



def order_cr_form(request):
    return {'order_cr_form': OrderCreateForm()}