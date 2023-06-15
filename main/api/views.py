from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BaseSettingsSerializer, ShopSetupSerializer

from accounts.models import UserProfile, LoyaltyCard, LoyaltyCardSettings, LoyaltyCardStatus
from blog.models import BlogSetup, BlogCategory, Post, PostBlock
from coupons.models import Coupon
from home.models import SliderSetup, Slider, Page
from orders.models import Order, OrderItem
from pay.models import PaymentSet, Yookassa, AlfaBank, PayKeeper, Tinkoff
from setup.models import BaseSettings, CustomCode, ThemeSettings, Colors
from shop.models import ShopSetup, PickupAreas, PayMethod, Category, Product, ProductImage, OptionType, ProductOption, OptionImage, AutoFieldOptions, CharGroup, CharName, ProductChar, Combo, ComboItem 
from subdomains.models import Subdomain



# Create your views here.
class BaseSettingsViewSet(viewsets.ModelViewSet):
    queryset = BaseSettings.objects.all()
    serializer_class = BaseSettingsSerializer


class ShopSetupViewSet(viewsets.ModelViewSet):
    queryset = ShopSetup.objects.all()
    serializer_class = ShopSetupSerializer