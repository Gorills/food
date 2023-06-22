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
from django.db.models import Sum
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class BaseSettingsViewSet(viewsets.ModelViewSet):
    queryset = BaseSettings.objects.all()
    serializer_class = BaseSettingsSerializer


class ShopSetupViewSet(viewsets.ModelViewSet):
    queryset = ShopSetup.objects.all()
    serializer_class = ShopSetupSerializer


@api_view(['GET'])
def get_statistic(request):
    products = Product.objects.all().count()
    orders = Order.objects.all().count()
    sales = Order.objects.all().aggregate(Sum('summ'))

    summ = sales['summ__sum']

    users = User.objects.all().exclude(is_staff=True)
    
    clients_reg = UserProfile.objects.filter(user__in=users).count()
    client_no_reg = UserProfile.objects.filter(user=None).count()

    clients = clients_reg+client_no_reg

    products = Product.objects.all().count()
    
    data = {
        'products': products,
        'orders': orders,
        'summ': summ,
        'clients': clients,
    }

    return Response(data, status=status.HTTP_200_OK)