from django.urls import include, path
from rest_framework import routers


from . import views
router = routers.DefaultRouter()
router.register(r'settings', views.BaseSettingsViewSet)
router.register(r'shop_settings', views.ShopSetupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('get_statistic/', views.get_statistic, name='get_statistic'),
   
   

]