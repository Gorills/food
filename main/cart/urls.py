from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<product_id>/', views.cart_add, name='cart_add'),
    path('remove/<product_id>/', views.cart_remove, name='cart_remove'),
    path('minus/<product_id>/', views.cart_minus, name='cart_minus'),
    path('plus/<product_id>/', views.cart_plus, name='cart_plus'),
    path('set_delivery/<int:value>/', views.set_delivery, name='set_delivery'),
    path('set_delivery_detail/', views.set_delivery_detail, name='set_delivery_detail'),
    
    
    path('active_balls/', views.active_balls, name='active_balls'),
    path('add_combo/', views.add_combo, name='add_combo'),
    path('remove_combo/', views.remove_combo, name='remove_combo'),
    path('plus_combo/', views.plus_combo, name='plus_combo'),
    path('minus_combo/', views.minus_combo, name='minus_combo'),

    path('add_options/', views.add_options, name='add_options'),
    path('remove_options/', views.remove_options, name='remove_options'),
    path('plus_options/', views.plus_options, name='plus_options'),
    path('minus_options/', views.minus_options, name='minus_options'),

    path('check_first_delivery/', views.check_first_delivery, name='check_first_delivery'),

    path('set_phone/', views.set_phone, name='set_phone'),
]