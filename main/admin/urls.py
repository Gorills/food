
from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin, name='admin'),
    path('general_settings/', views.general_settings, name='general_settings'),
    path('general_settings/email/', views.email_settings, name='email_settings'),
    path('general_settings/recaptcha/', views.recaptcha_settings, name='recaptcha_settings'),
    path('codes/', views.codes_settings, name='codes_settings'),
    path('codes/edit/<int:pk>/', views.codes_settings_edit, name='codes_settings_edit'),

    path('color_settings/', views.color_settings, name='color_settings'),
    path('theme_settings/', views.theme_settings, name='theme_settings'),

    # sale
    path('admin_order/', views.admin_order, name='admin_order'),
    path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('order_delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('order_status_change/<int:pk>/', views.order_status_change, name='order_status_change'),

    # sidebar
    path('sidebar_show/', views.sidebar_show, name='sidebar_show'),
    path('sidebar_hide/', views.sidebar_hide, name='sidebar_hide'),


    # promo
    path('promo/', views.admin_promo, name='admin_promo'),
    path('promo/add/', views.promo_add, name='promo_add'),
    path('promo/edit/<int:pk>/', views.promo_edit, name='promo_edit'),
    path('promo/delete/<int:pk>/', views.promo_delete, name='promo_delete'),

    # shop
    path('shop_settings/', views.shop_settings, name='shop_settings'),
    path('category/', views.admin_category, name='admin_category'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),

    path('product/', views.admin_product, name='admin_product'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),

    path('option_image/delete/<int:pk>/', views.option_image_delete, name='option_image_delete'),
    path('option/delete/<int:pk>/', views.option_delete, name='option_delete'),

    path('product_char/delete/<int:pk>/', views.product_char_delete, name='product_char_delete'),
    path('product_image/delete/<int:pk>/', views.product_image_delete, name='product_image_delete'),



    path('manufacturer/', views.admin_manufacturer, name='admin_manufacturer'),
    path('manufacturer/add/', views.manufacturer_add, name='manufacturer_add'),
    path('manufacturer/edit/<int:pk>/', views.manufacturer_edit, name='manufacturer_edit'),
    path('manufacturer/delete/<int:pk>/', views.manufacturer_delete, name='manufacturer_delete'),


    path('option_type/', views.admin_option_type, name='admin_option_type'),
    path('option_type/add/', views.option_type_add, name='option_type_add'),
    path('option_type/edit/<int:pk>/', views.option_type_edit, name='option_type_edit'),
    path('option_type/delete/<int:pk>/', views.option_type_delete, name='option_type_delete'),


    path('char/', views.admin_char, name='admin_char'),
    path('char/group/add', views.char_group_add, name='char_group_add'),
    path('char/group/edit/<int:pk>/', views.char_group_edit, name='char_group_edit'),
    path('char/group/delete/<int:pk>/', views.char_group_delete, name='char_group_delete'),

    path('char/add/', views.char_add, name='char_add'),
    path('char/edit/<int:pk>/', views.char_edit, name='char_edit'),
    path('char/delete/<int:pk>/', views.char_delete, name='char_delete'),



    # БЛОГ
    path('blog_settings/', views.blog_settings, name='blog_settings'),
    path('blog_category/', views.blog_category, name='blog_category'),
    path('blog_category/add/', views.blog_category_add, name='blog_category_add'),
    path('blog_category/edit/<int:pk>/', views.blog_category_edit, name='blog_category_edit'),
    path('blog_category/delete/<int:pk>/', views.blog_category_delete, name='blog_category_delete'),

    path('blog_post/', views.blog_post, name='blog_post'),
    path('blog_post/add/', views.post_add, name='post_add'),
    path('blog_post/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('blog_post/delete/<int:pk>/', views.post_delete, name='post_delete'),

    path('blog_post/draft/', views.post_draft, name='post_draft'),

    path('blog_post/post_block/', views.post_block, name='post_block'),
    path('blog_post/post_block/edit/<int:pk>/', views.post_block_edit, name='post_block_edit'),
    path('blog_post/post_block_edit/delete/<int:pk>/', views.post_block_edit_delete, name='post_block_edit_delete'),
    path('blog_post/post_block_add/delete/<int:pk>/', views.post_block_add_delete, name='post_block_add_delete'),



    # SLIDER
    path('static/slider/', views.admin_slider, name='admin_slider'),
    path('static/slider/add/', views.slider_add, name='slider_add'),
    path('static/slider/edit/<int:pk>/', views.slider_edit, name='slider_edit'),
    path('static/slider/delete/<int:pk>/', views.slider_delete, name='slider_delete'),


    # PAGES
    path('static/pages/', views.admin_pages, name='admin_pages'),
    path('static/pages/add/', views.page_add, name='page_add'),
    path('static/pages/edit/<int:pk>/', views.page_edit, name='page_edit'),



    # USERS
    path('users/', views.admin_users, name='admin_users'),
    path('users/delete/<int:pk>/', views.users_delete, name='users_delete'),



]


