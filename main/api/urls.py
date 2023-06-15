from django.urls import include, path
from rest_framework import routers
from .views import BaseSettingsViewSet, ShopSetupViewSet


from . import views
router = routers.DefaultRouter()
router.register(r'settings', BaseSettingsViewSet)
router.register(r'shop_settings', ShopSetupViewSet)


urlpatterns = [
    path('', include(router.urls)),
   
   

]