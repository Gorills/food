
from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('set_like/', views.set_like, name='set_like'),
    
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:parent>/<slug:slug>/', views.product_detail, name='product_detail'),
    

    # path('<slug:slug>/', views.category_detail, name='category_detail'),
    

]

