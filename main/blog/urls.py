
from django.urls import path
from . import views

urlpatterns = [

    path('', views.blog, name='blog'),
    path('<slug:slug>/', views.blog_category_detail, name='blog_category_detail'),
    path('<slug:parent>/<slug:slug>/', views.post_detail, name='post_detail'),

   
]


