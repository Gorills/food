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
    path('get_statistic/', views.get_statistic, name='get_statistic'),
    path('get_shop_settings/', views.get_shop_settings, name='get_shop_settings'),
    
   
   

]