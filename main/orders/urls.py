from django.urls import path
from . import views

from pay.models import PaymentSet



urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('callback/', views.order_callback, name='order_callback'),
    path('thank/', views.thank, name='thank'),
]


try:
    pay_name = PaymentSet.objects.get().name
except:
    pass

if pay_name == 'yookassa':
    urlpatterns.append(path('confirm/<int:pk>/', views.order_confirm, name='order_confirm')) 

if pay_name == 'paykeeper':
    urlpatterns.append(path('error/', views.order_error, name='order_error')) 
    urlpatterns.append(path('success/', views.order_success, name='order_success')) 