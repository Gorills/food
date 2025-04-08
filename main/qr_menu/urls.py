
from django.urls import path
from . import views


urlpatterns = [

    path('', views.qr_menu, name='qr_menu'),
    path('area/<int:pk>/', views.area_menu, name='area_menu'),
    path('table/<int:pk>/', views.table_menu, name='table_menu'),
    path('generage_area_qr/<int:pk>/', views.generate_area_qr, name='generate_area_qr'),
    path('generate_table_qr/<int:pk>/', views.generate_table_qr, name='generate_table_qr'),

    path('oficiant_call/<int:pk>/', views.oficiant_call, name='oficiant_call'),

    path('order/', views.order, name='qr_order'),
    path('order/success/<int:pk>/', views.order_success, name='order_success'),

]
