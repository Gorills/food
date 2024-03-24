
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *
from setup.models import BaseSettings
from . import views

sitemaps = {
    'static': StaticViewSitemap,
    'page': PageSitemap,
    'category': CategorySitemap,
    'product': ProductSitemap,
}


urlpatterns = [
    path('', views.home, name='home'),
    path('privacy/', views.privacy, name='privacy'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path("robots.txt", views.robots_txt),
    path('manifest.json', views.manifest_json, name='manifest_json'),

]


try:
    sms = BaseSettings.objects.get().sms
except:
    sms = ''

if sms:
    urlpatterns.append(path('login/', views.home_login, name='home_login')) 
    urlpatterns.append(path('logout/', views.home_logout, name='home_logout')) 

urlpatterns.append(path('<slug:slug>/', views.page_detail, name='page_detail')) 
