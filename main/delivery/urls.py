
from django.urls import path
from . import views
from .yandex_eda import check_price

urlpatterns = [

   path('check_order/', views.check_order, name='check_order'),
   path('check_price/', check_price, name='check_price'),

]
