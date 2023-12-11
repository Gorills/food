
from django.urls import path
from . import views

urlpatterns = [

   path('check_order/', views.check_order, name='check_order'),

]
