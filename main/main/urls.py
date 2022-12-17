
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('coupons/', include(('coupons.urls', 'coupons'), namespace='coupons')),
    path('catalog/', include('shop.urls')),
    path('blog/', include('blog.urls')),
    path('admin/', include('admin.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('yafeed/', include('yafeed.urls')),
    


    # Внизу, потому что url модели Page должны обрабатываться последними
    path('', include('home.urls')),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "home.views.page_not_found_view"