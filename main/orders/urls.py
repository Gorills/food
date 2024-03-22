from django.urls import path
from . import views
from . import order_fast
from pay.models import PaymentSet



urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('create/fast/', order_fast.order_create, name='order_create_fast'),
    path('callback/', views.order_callback, name='order_callback'),
    path('thank/', views.thank, name='thank'),
    path('alpha_check/<int:pk>/', views.alpha_check, name='alpha_check'),
]


try:
    pay_name = PaymentSet.objects.get().name
except:
    pay_name = ''

if pay_name == 'yookassa':
    urlpatterns.append(path('confirm/<int:pk>/', views.order_confirm, name='order_confirm')) 
    urlpatterns.append(path('confirm/', views.order_webhook, name='order_webhook')) 

if pay_name == 'alfabank':
    urlpatterns.append(path('error/', views.order_error, name='order_error')) 
    urlpatterns.append(path('success/', views.order_success, name='order_success')) 

if pay_name == 'paykeeper':
    urlpatterns.append(path('paykeeper/fail/', views.paykeeper_error, name='paykeeper_error')) 
    urlpatterns.append(path('paykeeper/success/', views.paykeeper_success, name='paykeeper_success')) 
    urlpatterns.append(path('paykeeper/session/<int:pk>/', views.paykeeper_session, name='paykeeper_session')) 


if pay_name == 'tinkoff':
    urlpatterns.append(path('error/', views.order_error, name='order_error')) 
    urlpatterns.append(path('tinkoff_success/<int:pk>/', views.tinkoff_success, name='tinkoff_success')) 