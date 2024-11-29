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
router.register(r'orders', views.OrderSet,basename='order')



urlpatterns = [
    
    path('first_delivery/<str:number>/', views.first_delivery, name='first_delivery'),
    path('get_statistic/', views.get_statistic, name='get_statistic'),
    path('get_shop_settings/', views.get_shop_settings, name='get_shop_settings'),
    path('related_products/', views.related_products, name='related_products'),
    path('get_cart_products/', views.get_cart_products, name='get_cart_products'),
    path('get_user/', views.get_user, name='get_user'),
    path('get_work_active/<int:day>/', views.get_work_active, name='get_work_active'),
    path('get_order_status/<int:pk>/', views.get_order_status, name='get_order_status'),
    path('dop_items/', views.dop_items, name='dop_items'),
    path('orderview/<int:order_id>/', views.OrderViewList.as_view(), name='orderview-list'),
    path('check_promo/', views.check_promo, name='check_promo'),
    path('get_exclude_actions/<int:pk>/', views.get_exclude_actions, name='get_exclude_actions'),
    path('send-sms-code/', views.send_sms_code, name='send_sms_code'),
    path('verify-sms-code/', views.verify_sms_code, name='verify_sms_code'),
    path('logout/', views.logout, name='logout'),
    path('check-session/', views.check_session, name='check_session'),
   
   

] + router.urls