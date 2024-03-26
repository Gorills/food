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

from .get_work_day import get_hours

from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from cart.cart import delivery_time_price







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


def normalize_phone_number(phone_number):
    # Заменяем специальные символы на соответствующие значения
    normalized_number = phone_number.replace('%20', ' ').replace('%28', '(').replace('%29', ')')
    return normalized_number


@api_view(['GET'])
def first_delivery(request, number):

    normal_number = normalize_phone_number(number)
    print(normal_number)
    orders = Order.objects.filter(phone=normal_number).count()
    

    if orders == 0:
        first_delivery = True
    else:
        first_delivery = False

    return Response(first_delivery)

    



@api_view(['GET'])
def get_shop_settings(request):
    general_settings = BaseSettings.objects.first()
    settings = ShopSetup.objects.first()
    pay_methods = PayMethod.objects.all()
    pickup_areas = PickupAreas.objects.all()
    try:
        pay = PaymentSet.objects.first().status
        if pay:
            pay_online = True
        else:
            pay_online = False
    except:
        pay_online = False
    

    pay_methods_arr = []

    for pay_method in pay_methods:
        pay_methods_arr.append({
           
            'name': pay_method.name,
            'in_pay_delivery': pay_method.in_pay_delivery,
            'in_pay_pickup': pay_method.in_pay_pickup
        })
    
    if not pay_methods_arr:

        if settings.only_pay_with_delivery:
            in_pay_delivery = False
        else:
            in_pay_delivery = True
       
        pay_methods_arr.append({
            'name': 'Картой при получении',
            'in_pay_delivery': in_pay_delivery,
            'in_pay_pickup': True
        })

        pay_methods_arr.append({
            'name': 'Наличными при получении',
            'in_pay_delivery': in_pay_delivery,
            'in_pay_pickup': True
        })

    if pay_online:
        pay_methods_arr.append({
            'name': 'Картой на сайте',
            'in_pay_delivery': True,
            'in_pay_pickup': True
        })


    pickup_areas_arr = []

    for pickup_area in pickup_areas:
        pickup_areas_arr.append({
            'name': pickup_area.name
        })

    
    if not pickup_areas_arr:
        pickup_areas_arr.append({
            'name': general_settings.address
        })

    hours = get_hours(request)



    item = {
        
        'price_delivery': delivery_time_price()['price_delivery'],
        'free_delivery': delivery_time_price()['free_delivery'],
        'min_delivery': delivery_time_price()['min_delivery'],
        'zones_delivery': settings.zones_delivery,
        'hide_delivery_choosing': settings.hide_delivery_choosing,
        'first_delivery': settings.first_delivery,
        'discount_on_pickup': settings.discount_on_pickup,
        'summ_discount': settings.summ_discount,

        
        'pay_methods': pay_methods_arr,
        'pickup_areas': pickup_areas_arr,
        'work_hours': hours,
    }

    return Response(item, status=status.HTTP_200_OK)



@api_view(['GET'])
def related_products(request):

    related_products = Product.objects.filter(related=True, status=True)


    items = []



    for related in related_products:

        
        items.append({
            'id': related.id,
            'name': related.name,
            
            'price': related.price,
            'image': related.get_thumb_mini(),
            'free': related.free,
            

        })

    
    data = {
        'items': items
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user(request):
    try:
        user_id = request.session['user_profile_id']
        user = UserProfile.objects.get(id=user_id)
        data = {
            'phone': user.phone
        }
        return Response(data, status=status.HTTP_200_OK)
    except KeyError:
        return Response({'phone': 'error'}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({'phone': 'error'}, status=status.HTTP_200_OK)





# !!! Is admin !!! 
from sms.views import send_sms
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    

    def perform_update(self, serializer):
        # Вызываем вашу стороннюю функцию для обработки данных

        order_id = self.kwargs['pk']
        

        if not getattr(self, 'reverted_status_actions_done', False):
            self.process_data(order_id, self.request.POST)
            setattr(self, 'reverted_status_actions_done', True)

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
            
            if loyalty_settings.status_up == True:
                if order_count == 1 and enable_add_balls_after_first_order and order.summ >= first_order_summ_for_add_balls:
                    card.balls = card.balls + balls_after_first_order
                    card.summ = Decimal(card.summ) + (Decimal(order.summ) - Decimal(order.delivery_price))
                    balls_summ = balls_after_first_order


                
                else:
                
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

                if loyalty_settings.status_up == True:

                    if order_count == 1 and enable_add_balls_after_first_order and order.summ >= first_order_summ_for_add_balls:
                        card.balls = card.balls - balls_after_first_order
                        card.summ = Decimal(card.summ) - (Decimal(order.summ) - Decimal(order.delivery_price))
                    else:
                        
                        card.summ = Decimal(card.summ) - (Decimal(order.summ) - Decimal(order.delivery_price))
                        card.balls = card.balls - (((Decimal(order.summ) - Decimal(order.delivery_price)) / 100) * card.status().percent_up).quantize(Decimal("1"), ROUND_DOWN) 


        card.save()


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



