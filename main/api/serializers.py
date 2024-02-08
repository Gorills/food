from rest_framework import serializers
from accounts.models import UserProfile, LoyaltyCard, LoyaltyCardSettings, LoyaltyCardStatus
from blog.models import BlogSetup, BlogCategory, Post, PostBlock
from coupons.models import Coupon
from home.models import SliderSetup, Slider, Page
from orders.models import Order, OrderItem
from pay.models import PaymentSet, Yookassa, AlfaBank, PayKeeper, Tinkoff
from setup.models import BaseSettings, CustomCode, ThemeSettings, Colors
from shop.models import ShopSetup, PickupAreas, PayMethod, Category, Product, ProductImage, OptionType, ProductOption, OptionImage, AutoFieldOptions, CharGroup, CharName, ProductChar, Combo, ComboItem 
from subdomains.models import Subdomain


# Базовые настройки сайта





class BaseSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSettings
        fields = '__all__'


class ShopSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSetup
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionImage
        fields = '__all__'

class ProductOptionSerializer(serializers.ModelSerializer):
    option_images = OptionImageSerializer(many=True, read_only=True)
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
        fields = '__all__'