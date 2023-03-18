from django.urls import path
from . import views


urlpatterns = [
    # path('', views.cart_detail, name='cart_detail'),
    path('add/<product_id>/', views.cart_add, name='cart_add'),
    path('remove/<product_id>/', views.cart_remove, name='cart_remove'),
    path('minus/<product_id>/', views.cart_minus, name='cart_minus'),
    path('plus/<product_id>/', views.cart_plus, name='cart_plus'),
    path('set_delivery/<int:value>/', views.set_delivery, name='set_delivery'),
    path('delivery_summ/<int:value>/', views.delivery_summ, name='delivery_summ'),
    path('active_balls/', views.active_balls, name='active_balls'),
    path('add_combo/', views.add_combo, name='add_combo'),
    path('remove_combo/', views.remove_combo, name='remove_combo'),
    path('plus_combo/', views.plus_combo, name='plus_combo'),
    path('minus_combo/', views.minus_combo, name='minus_combo'),
]