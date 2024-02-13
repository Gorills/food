from decimal import Decimal, ROUND_DOWN
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BaseSettingsSerializer, ComboSerializer, FoodConstructorSerializer, OrderSerializer, ShopSetupSerializer, CategorySerializer, ProductSerializer

from accounts.models import UserProfile, LoyaltyCard, LoyaltyCardSettings, LoyaltyCardStatus
from blog.models import BlogSetup, BlogCategory, Post, PostBlock
from coupons.models import Coupon
from home.models import SliderSetup, Slider, Page
from orders.models import Order, OrderItem
from pay.models import PaymentSet, Yookassa, AlfaBank, PayKeeper, Tinkoff
from setup.models import BaseSettings, CustomCode, ThemeSettings, Colors
from shop.models import FoodConstructor, ShopSetup, PickupAreas, PayMethod, Category, Product, ProductImage, OptionType, ProductOption, OptionImage, AutoFieldOptions, CharGroup, CharName, ProductChar, Combo, ComboItem 
from shop.models import WorkDay
from subdomains.models import Subdomain


from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes






# !!! All users !!!

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.filter(related=False, status=True)
    serializer_class = ProductSerializer


class ComboViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer


class FoodConstructorSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = FoodConstructor.objects.all()
    serializer_class = FoodConstructorSerializer


# !!! Is admin !!! 
from sms.views import send_sms
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        # Вызываем вашу стороннюю функцию для обработки данных

        order_id = self.kwargs['pk']
        self.process_data(order_id, self.request.POST)

        # Продолжаем обновление объекта Order
        serializer.save()

    def process_data(self, order_id, post_data):

        order = Order.objects.get(id=order_id)
        order_prev_status = order.status
        loyalty_settings = LoyaltyCardSettings.objects.get()
        
        user = order.user_pr
        card = LoyaltyCard.objects.get(user=user)
        user_orders = Order.objects.filter(user_pr=user)

        order_count = user_orders.count()

        status = post_data['status']

        enable_add_balls_after_first_order = loyalty_settings.enable_add_balls_after_first_order
        balls_after_first_order = loyalty_settings.balls_after_first_order
        first_order_summ_for_add_balls = loyalty_settings.first_order_summ_for_add_balls
        send_sms_status = loyalty_settings.send_sms
        sms_text = loyalty_settings.sms_text
        balls_summ = 0
        if status == 'Выполнен':
            
            if order_count == 1 and enable_add_balls_after_first_order and order.summ >= first_order_summ_for_add_balls:
                card.balls = card.balls + balls_after_first_order
                card.summ = Decimal(card.summ) + (Decimal(order.summ) - Decimal(order.delivery_price))
                balls_summ = balls_after_first_order


            
            else:
                if loyalty_settings.status_up == True:
                    card.summ = Decimal(card.summ) + (Decimal(order.summ) - Decimal(order.delivery_price))
                    card.balls = card.balls + (((Decimal(order.summ) - Decimal(order.delivery_price)) / 100) * card.status().percent_up).quantize(Decimal("1"), ROUND_DOWN) 
                    balls_summ = (((Decimal(order.summ) - Decimal(order.delivery_price)) / 100) * card.status().percent_up).quantize(Decimal("1"), ROUND_DOWN) 



            if send_sms_status == True:
                try:
                    site_name = BaseSettings.objects.get().name
                except:
                    site_name = ''    
                
                if site_name:
                    sms_text = sms_text.replace('{balls}', str(balls_summ)).replace('{sitename}', site_name)
                else:
                    sms_text = sms_text.replace('{balls}', str(balls_summ)).replace('- {sitename}', '')
                phone = order.phone
                if balls_summ != 0:
                    send_sms(sms_text, phone)
                

        if status == 'Отказ':
            
            if order_prev_status == 'Выполнен':
                
                if order_count == 1 and enable_add_balls_after_first_order and order.summ >= first_order_summ_for_add_balls:
                    card.balls = card.balls - balls_after_first_order
                    card.summ = Decimal(card.summ) - (Decimal(order.summ) - Decimal(order.delivery_price))
                else:
                    if loyalty_settings.status_up == True:
                        card.summ = Decimal(card.summ) - (Decimal(order.summ) - Decimal(order.delivery_price))
                        card.balls = card.balls - (((Decimal(order.summ) - Decimal(order.delivery_price)) / 100) * card.status().percent_up).quantize(Decimal("1"), ROUND_DOWN) 


        card.save()


        
        pass

class BaseSettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = BaseSettings.objects.all()
    serializer_class = BaseSettingsSerializer


class ShopSetupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ShopSetup.objects.all()
    serializer_class = ShopSetupSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statistic(request):
    
    products = Product.objects.all().count()
    orders = Order.objects.filter(status='Выполнен').count()
    sales = Order.objects.filter(status='Выполнен').aggregate(Sum('summ'))

    summ_res = sales['summ__sum']

    if summ_res:
        res = summ_res
    else:
        res = 0

    users = User.objects.all().exclude(is_staff=True)
    
    clients_reg = UserProfile.objects.filter(user__in=users).count()
    client_no_reg = UserProfile.objects.filter(user=None).count()

    clients = clients_reg+client_no_reg

    products = Product.objects.all().count()
    
    items = [
        { 'id': 1, 'count': str(orders), 'name': 'заказов', 'icons': 'basket' },
        { 'id': 2, 'count': str(res), 'name': 'продаж', 'icons': 'card' },
        { 'id': 3, 'count': str(products), 'name': 'товаров', 'icons': 'product' },
        { 'id': 4, 'count': str(clients), 'name': 'клиентов', 'icons': 'users' },
    ]

    
    return Response(items, status=status.HTTP_200_OK)



