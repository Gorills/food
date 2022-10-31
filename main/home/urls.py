
from django.urls import path


from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),


    path("robots.txt", views.robots_txt),
]

