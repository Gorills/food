
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

from . import views

sitemaps = {
    'static': StaticViewSitemap,
    'page': PageSitemap,
    'category': CategorySitemap,
    'product': ProductSitemap,
}


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path("robots.txt", views.robots_txt),
    path('<slug:slug>/', views.page_detail, name='page_detail'),

]

