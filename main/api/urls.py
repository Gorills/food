from django.urls import include, path
from rest_framework import routers


from . import views
router = routers.DefaultRouter()

# !!! All users !!!
router.register(r'categorys', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'combos', views.ComboViewSet)
router.register(r'constructors', views.FoodConstructorSet)


# !!! Is admin !!!
router.register(r'settings', views.BaseSettingsViewSet)
router.register(r'shop_settings', views.ShopSetupViewSet)
router.register(r'orders', views.OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('first_delivery/<str:number>/', views.first_delivery, name='first_delivery'),
    path('get_statistic/', views.get_statistic, name='get_statistic'),
    path('get_shop_settings/', views.get_shop_settings, name='get_shop_settings'),
    path('related_products/', views.related_products, name='related_products'),
    path('get_user/', views.get_user, name='get_user'),
    path('get_work_active/<int:day>/', views.get_work_active, name='get_work_active'),
    
   
   

]