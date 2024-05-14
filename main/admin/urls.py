
from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin, name='admin'),
    path('get_workers/', views.get_workers, name='get_workers'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit_user_rights/<int:user_id>/', views.edit_user_rights, name='edit_user_rights'),

    path('general_settings/', views.general_settings, name='general_settings'),
    path('general_settings/block/', views.general_settings_block, name='general_settings_block'),
    path('general_settings/email/', views.email_settings, name='email_settings'),
    path('general_settings/recaptcha/', views.recaptcha_settings, name='recaptcha_settings'),
    path('codes/', views.codes_settings, name='codes_settings'),
    path('codes/edit/<int:pk>/', views.codes_settings_edit, name='codes_settings_edit'),
    path('codes/delete/<int:pk>/', views.codes_settings_delete, name='codes_settings_delete'),

    path('color_settings/', views.color_settings, name='color_settings'),
    path('theme_settings/', views.theme_settings, name='theme_settings'),
    path('font_settings/', views.font_settings, name='font_settings'),

    # sale
    path('admin_order/', views.admin_order, name='admin_order'),
    path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('order_delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('order_status_change/<int:pk>/', views.order_status_change, name='order_status_change'),
    path('order_view_all/', views.order_view_all, name='order_view_all'),
    path('order_status/', views.order_status, name='order_status'),
    path('add_order_status/', views.add_order_status, name='add_order_status'),
    path('edit_order_status/<int:pk>/', views.edit_order_status, name='edit_order_status'),
    path('delete_order_status/<int:pk>/', views.delete_order_status, name='delete_order_status'),



    # payments
    path('admin_payments/', views.admin_payments, name='admin_payments'),
    path('yookassa_save/', views.yookassa_save, name='yookassa_save'),
    path('alfabank_save/', views.alfabank_save, name='alfabank_save'),
    path('paykeeper_save/', views.paykeeper_save, name='paykeeper_save'),
    path('tinkoff_save/', views.tinkoff_save, name='tinkoff_save'),

    # delivery
    path('admin_delivery/', views.admin_delivery, name='admin_delivery'),
    path('delivery_add/', views.delivery_add, name='delivery_add'),
    path('delivery_edit/<int:pk>/', views.delivery_edit, name='delivery_edit'),
    path('delivery_delete/<int:pk>/', views.delivery_delete, name='delivery_delete'),

    # paay method
    path('add_pay_method/', views.add_pay_method, name='add_pay_method'),
    path('edit_pay_method/<int:pk>/', views.edit_pay_method, name='edit_pay_method'),
    path('delete_pay_method/<int:pk>/', views.delete_pay_method, name='delete_pay_method'),

    

    # sidebar
    path('sidebar_show/', views.sidebar_show, name='sidebar_show'),
    path('sidebar_hide/', views.sidebar_hide, name='sidebar_hide'),


    # promo
    path('promo/', views.admin_promo, name='admin_promo'),
    path('promo/add/', views.promo_add, name='promo_add'),
    path('promo/edit/<int:pk>/', views.promo_edit, name='promo_edit'),
    path('promo/delete/<int:pk>/', views.promo_delete, name='promo_delete'),


    # loyalty card
    path('admin_card/', views.admin_card, name='admin_card'),
    path('card_settings/', views.card_settings, name='card_settings'),
    path('card_add/', views.card_add, name='card_add'),
    path('card_edit/<int:pk>/', views.card_edit, name='card_edit'),
    path('card_delete/<int:pk>/', views.card_delete, name='card_delete'),


    path('loyalty_card_status_edit/<int:pk>/', views.loyalty_card_status_edit, name='loyalty_card_status_edit'),
    path('loyalty_card_status_delete/<int:pk>/', views.loyalty_card_status_delete, name='loyalty_card_status_delete'),


    # reviews
    path('admin_reviews/', views.admin_reviews, name='admin_reviews'),
    path('add_reviews/', views.add_reviews, name='add_reviews'),
    path('edit_reviews/<int:pk>/', views.edit_reviews, name='edit_reviews'),
    path('delete_reviews/<int:pk>/', views.delete_reviews, name='delete_reviews'),


    # CSV UPLOAD
    path('csv_upload/', views.csv_upload, name='csv_upload'),
    
    # zone file
    path('zone_file/', views.zone_file, name='zone_file'),


    # pickup zones
    path('add_zone/', views.add_zone, name='add_zone'),
    path('edit_zone/<int:pk>/', views.edit_zone, name='edit_zone'),
    path('delete_zone/<int:pk>/', views.delete_zone, name='delete_zone'),


    # district setup
    path('district_setup/', views.district_setup, name='district_setup'),


    # shop
    path('shop_settings/', views.shop_settings, name='shop_settings'),
    path('dop_items/add/', views.dop_items_add, name='dop_items_add'),
    path('dop_items/edit/<int:pk>/', views.dop_items_edit, name='dop_items_edit'),
    path('dop_items/delete/<int:pk>/', views.dop_items_delete, name='dop_items_delete'),

    path('category/', views.admin_category, name='admin_category'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('category/orderby_edit/<int:pk>/', views.cat_orderby_edit, name='cat_orderby_edit'),

    path('product/', views.admin_product, name='admin_product'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product/save_us/<int:pk>/', views.product_save_as, name='product_save_as'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),

    path('admin_sale/', views.admin_sale, name='admin_sale'),
    path('add_sale/', views.add_sale, name='add_sale'),
    path('edit_sale/<int:pk>/', views.edit_sale, name='edit_sale'),
    path('delete_sale/<int:pk>/', views.delete_sale, name='delete_sale'),

    path('admin_food_constructor/', views.admin_food_constructor, name='admin_food_constructor'),
    path('add_food_constructor/', views.add_food_constructor, name='add_food_constructor'),
    path('edit_food_constructor/<int:pk>/', views.edit_food_constructor, name='edit_food_constructor'),
    path('delete_food_constructor/<int:pk>/', views.delete_food_constructor, name='delete_food_constructor'),

    path('add_constructor_category/<int:pk>/', views.add_constructor_category, name='add_constructor_category'),
    path('edit_constructor_category/<int:pk>/', views.edit_constructor_category, name='edit_constructor_category'),
    path('delete_constructor_category/<int:pk>/', views.delete_constructor_category, name='delete_constructor_category'),
    path('add_ingridients/<int:pk>/', views.add_ingridients, name='add_ingridients'),
    path('edit_ingridients/<int:pk>/', views.edit_ingridients, name='edit_ingridients'),
    path('delete_ingridients/<int:pk>/', views.delete_ingridients, name='delete_ingridients'),




    # works day
    
    path('add_worksday/', views.add_worksday, name='add_worksday'),
    path('edit_worksday/<int:pk>/', views.edit_worksday, name='edit_worksday'),
    path('delete_worksday/<int:pk>/', views.delete_worksday, name='delete_worksday'),

    # delivery time prices
    path('delivery_time_price/', views.delivery_time_price, name='delivery_time_price'),
    path('add_delivery_time_price/', views.add_delivery_time_price, name='add_delivery_time_price'),
    path('edit_delivery_time_price/<int:pk>/', views.edit_delivery_time_price, name='edit_delivery_time_price'),
    path('delete_delivery_time_price/<int:pk>/', views.delete_delivery_time_price, name='delete_delivery_time_price'),
  

    # Комбо
    path('combo/', views.admin_combo, name='admin_combo'),
    path('add_combo/', views.add_combo, name='add_combo'),
    path('edit_combo/<int:pk>/', views.edit_combo, name='edit_combo'),
    path('delete_combo/<int:pk>/', views.delete_combo, name='delete_combo'),

    path('delete_combo_item/<int:pk>/', views.delete_combo_item, name='delete_combo_item'),

    
    

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

    path('option_autofield/add/', views.option_autofield_add, name='option_autofield_add'),
    path('option_autofield/edit/<int:pk>/', views.option_autofield_edit, name='option_autofield_edit'),
    path('option_autofield/remove/<int:pk>/', views.option_autofield_delete, name='option_autofield_delete'),
    path('option_autofield/detail/<int:pk>/', views.option_autofield_detail, name='option_autofield_detail'),


    path('char/', views.admin_char, name='admin_char'),
    path('char/group/add', views.char_group_add, name='char_group_add'),
    path('char/group/edit/<int:pk>/', views.char_group_edit, name='char_group_edit'),
    path('char/group/delete/<int:pk>/', views.char_group_delete, name='char_group_delete'),

    path('char/add/', views.char_add, name='char_add'),
    path('char/edit/<int:pk>/', views.char_edit, name='char_edit'),
    path('char/delete/<int:pk>/', views.char_delete, name='char_delete'),


    # Сопутствующие товары
    path('related/', views.related, name='related'),

    path('related/add/', views.related_add, name='related_add'),
    path('related_edit/edit/<int:pk>/', views.related_edit, name='related_edit'),
    path('related_delete/delete/<int:pk>/', views.related_delete, name='related_delete'),

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
    path('static/pages/delete/<int:pk>/', views.page_delete, name='page_delete'),

    path('static/pages/page_item_add/<int:pk>/', views.page_item_add, name='page_item_add'),
    path('static/pages/page_item_edit/<int:pk>/', views.page_item_edit, name='page_item_edit'),
    path('static/pages/page_item_delete/<int:pk>/', views.page_item_delete, name='page_item_delete'),

    # IMAGES
    path('static/images/', views.admin_images, name='admin_images'),
    path('static/images/add/', views.image_add, name='image_add'),
    path('static/images/edit/<int:pk>/', views.image_edit, name='image_edit'),
    path('static/images/delete/<int:pk>/', views.image_delete, name='image_delete'),

    # USERS
    path('users/', views.admin_users, name='admin_users'),
    path('users/delete/<int:pk>/', views.users_delete, name='users_delete'),
    path('users/detail/<int:pk>/', views.users_detail, name='users_detail'),



    # FAQ
    path('faq/', views.faq, name='faq'),

    # SUBDOMAINS
    path('admin_subdomain/', views.admin_subdomain, name='admin_subdomain'),
    path('admin_subdomain/add/', views.add_subdomain, name='add_subdomain'),
    path('admin_subdomain/edit/<int:pk>/', views.edit_subdomain, name='edit_subdomain'),
    path('admin_subdomain/delete/<int:pk>/', views.delete_subdomain, name='delete_subdomain'),


    # INTEGRATIONS
    path('integration/', views.integration, name='integration'),
    path('integration/add/', views.add_integration, name='add_integration'),
    path('integration/edit/<int:pk>/', views.edit_integration, name='edit_integration'),
    path('integration/delete/<int:pk>/', views.delete_integration, name='delete_integration'),



    path('catalogs_synch/', views.catalogs_synch, name='catalogs_synch'),
    path('synch_cron/', views.synch_cron, name='synch_cron'),





]


