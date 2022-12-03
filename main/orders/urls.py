from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('confirm/<int:pk>/', views.order_confirm, name='order_confirm'),
    path('callback/', views.order_callback, name='order_callback'),
    path('thank/', views.thank, name='thank'),
]