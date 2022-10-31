from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<product_id>/', views.cart_add, name='cart_add'),
    path('remove/<product_id>/', views.cart_remove, name='cart_remove'),
    path('minus/<product_id>/', views.cart_minus, name='cart_minus'),
    path('plus/<product_id>/', views.cart_plus, name='cart_plus'),
]