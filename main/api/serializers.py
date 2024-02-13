from rest_framework import serializers
from accounts.models import UserProfile, LoyaltyCard, LoyaltyCardSettings, LoyaltyCardStatus
from blog.models import BlogSetup, BlogCategory, Post, PostBlock
from coupons.models import Coupon
from home.models import SliderSetup, Slider, Page
from orders.models import Order, OrderItem
from pay.models import PaymentSet, Yookassa, AlfaBank, PayKeeper, Tinkoff
from setup.models import BaseSettings, CustomCode, ThemeSettings, Colors
from shop.models import ConstructorCategory, FoodConstructor, Ingridients, ShopSetup, PickupAreas, PayMethod, Category, Product, ProductImage, OptionType, ProductOption, OptionImage, AutoFieldOptions, CharGroup, CharName, ProductChar, Combo, ComboItem 
from subdomains.models import Subdomain




# all users







class OptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionImage
        fields = '__all__'

class OptionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionType
        fields = [
            'option_class'
        ]

class ProductOptionSerializer(serializers.ModelSerializer):
    option_images = OptionImageSerializer(many=True, read_only=True)
    type = OptionTypeSerializer()
    class Meta:
        model = ProductOption
        fields = '__all__'

class CharGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharGroup
        fields = ['name']

class CharNameSerializer(serializers.ModelSerializer):
    group = CharGroupSerializer()

    class Meta:
        model = CharName
        fields = ['text_name', 'group']

class ProductCharSerializer(serializers.ModelSerializer):
    char_name = CharNameSerializer()
    class Meta:
        model = ProductChar
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True, read_only=True)
    chars = ProductCharSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Product
        fields = [
            'id',
            'external_id',
            'name',
            'short_description',
            'description',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'price',
            'old_price',
            'stock',
            'sales',
            'minimum',
            'new',
            'bestseller',
            'slug',
            'length',
            'width',
            'height',
            'length_class',
            'weight',
            'weight_class',
            'thumb',
            'sort_order',



            
            'chars',
            'options',
            'parent',
        ]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = [
            'external_id',
            'id',
            'name',
            'description',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'top',
            'home',
            'resize',
            'font_color',
            'bg_color',
            'opacity',
            'column',
            'sort_order',
            'status',
            'slug',
            'parent',
            'products'

        ]


class ComboItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboItem
        fields = '__all__'


class ComboSerializer(serializers.ModelSerializer):
    items = ComboItemSerializer(many=True, read_only=True)
    class Meta:
        model = Combo
        fields = '__all__'



class IngridientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridients
        fields = '__all__'


class ConstructorCategorySerializer(serializers.ModelSerializer):
    ingridients = IngridientsSerializer(many=True, read_only=True)
    class Meta:
        model = ConstructorCategory
        fields = '__all__'



class FoodConstructorSerializer(serializers.ModelSerializer):
    constructor_categorys = ConstructorCategorySerializer(many=True, read_only=True)
    parent = CategorySerializer(read_only=True)
    class Meta:
        model = FoodConstructor
        fields = '__all__'


# Базовые настройки сайта
# is admin
        
class ShopSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSetup
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class BaseSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSettings
        fields = '__all__'

