from django.urls import include, path
from rest_framework import routers
from .views import BaseSettingsViewSet


from . import views
router = routers.DefaultRouter()
router.register(r'settings', BaseSettingsViewSet)


urlpatterns = [
    path('', include(router.urls)),
   
   

]