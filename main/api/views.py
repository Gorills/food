from decimal import Decimal, ROUND_DOWN
from actions.models import Action
from orders.telegram import send_message
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pytils.translit import slugify

from .serializers import ActionSerializer, BaseSettingsSerializer, ComboSerializer, DopItemsSerializer, FoodConstructorSerializer, OrderSerializer, OrderViewSerializer, ShopSetupSerializer, CategorySerializer, ProductSerializer

from accounts.models import UserProfile, LoyaltyCard, LoyaltyCardSettings, LoyaltyCardStatus
from blog.models import BlogSetup, BlogCategory, Post, PostBlock
from coupons.models import Coupon
from home.models import SliderSetup, Slider, Page
from orders.models import Order, OrderItem, OrderView
from pay.models import PaymentSet, Yookassa, AlfaBank, PayKeeper, Tinkoff
from setup.models import BaseSettings, CustomCode, ThemeSettings, Colors
from shop.models import DopItems, FoodConstructor, ShopSetup, PickupAreas, PayMethod, Category, Product, ProductImage, OptionType, ProductOption, OptionImage, AutoFieldOptions, CharGroup, CharName, ProductChar, Combo, ComboItem 
from shop.models import WorkDay
from subdomains.models import Subdomain
from subdomains.utilites import get_subdomain

from .get_work_day import get_hours

from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from cart.cart import delivery_time_price
import random

from django.core.cache import cache
from django.http import JsonResponse
import re


# !!! All users !!!



def normalize_phone(phone):
    """Нормализует номер телефона для использования в качестве ключа кеша."""
    return re.sub(r'[^\d+]', '', phone)  # Убираем все символы, кроме цифр и '+'



def send_sms_code(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        phone = data.get("phone")

        if not phone:
            return JsonResponse({"success": False, "message": "Phone number is required"}, status=400)

        normalized_phone = normalize_phone(phone)  # Нормализуем номер телефона

        # Генерация кода
        code = random.randint(1000, 9999)

        # Сохраняем код в кэш с TTL 5 минут
        cache_key = f"sms_code_{normalized_phone}"
        cache.set(cache_key, code, timeout=300)
        text = 'Ваш код: ' + str(code)
        send_sms(text, phone)

        # Отправка SMS (заглушка)
        # print(f"Отправлен код {code} на номер {phone}")  # Реализуйте интеграцию с SMS-сервисом

        return JsonResponse({"success": True, "message": "Code sent successfully"})

    return JsonResponse({"success": False, "message": "Only POST method is allowed"}, status=405)

def add_loyalty_card(userprofile):
    try:
        card_active = LoyaltyCardSettings.objects.get().active
    except:
        card_active = False
        
    if card_active == True:            
        try:
            loyalty_card = LoyaltyCard.objects.get(user=userprofile)

        except Exception as e:
            summ = ShopSetup.objects.get().start_bonus
            loyalty_card = LoyaltyCard(
                user=userprofile,
                summ=Decimal(0),
                balls=Decimal(summ),
                )
            
            loyalty_card.save()

def verify_sms_code(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        phone = data.get("phone")
        code = data.get("code")

        if not phone or not code:
            return JsonResponse({"success": False, "message": "Phone and code are required"}, status=400)

        normalized_phone = normalize_phone(phone)
        # Получаем код из кэша
        cached_code = cache.get(f"sms_code_{normalized_phone}")

        if str(cached_code) == str(code):
            try:
                userprofile = UserProfile.objects.get(phone=phone)
                userprofile.use_sms = True
                userprofile.save()
            except:
                userprofile = UserProfile(phone=phone, use_sms = True)
                userprofile.save()

            add_loyalty_card(userprofile)
            request.session['user_profile_id'] = userprofile.id

            return JsonResponse({"success": True, "message": "Verification successful"})
        else:
            return JsonResponse({"success": False, "message": "Invalid code"}, status=401)

    return JsonResponse({"success": False, "message": "Only POST method is allowed"}, status=405)




def check_session(request):
    # Проверяем, есть ли у пользователя активная сессия
    try:
        request.session['user_profile_id']
    except:
        return JsonResponse({"isAuthenticated": False})
    
    id = request.session['user_profile_id']
    user = UserProfile.objects.filter(id=id).first()
    if user is None:
        return JsonResponse({"isAuthenticated": False})
    else:
        return JsonResponse({"isAuthenticated": True})

def logout(request):
    if request.method == "GET":
        request.session.flush()
        return JsonResponse({"success": True, "message": "Logout successful"})
    return JsonResponse({"success": False, "message": "Only POST method is allowed"}, status=405)



class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.filter(status=True)
    serializer_class = ProductSerializer


@api_view(['GET'])
def actions(request):
    actions = Action.objects.filter(active=True)
    serializer = ActionSerializer(actions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_exclude_actions(request, pk):

    product = Product.objects.get(id=pk)

    data = {
        'exclude': product.parent.exclude_actions
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_cart_products(request):
    products = Product.objects.filter(in_cart=True, status=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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

    normal_number = normalize_phone_number(number).replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('+', '')

    if normal_number[0] == '8' and len(normal_number) == 11:
        normal_number = '7' + normal_number[1:]

    normal_number = '+'+normal_number[0]+' ('+normal_number[1:4]+') '+normal_number[4:7]+' '+normal_number[7:9]+'-'+normal_number[9:]
        

    

    orders = Order.objects.filter(phone=normal_number, status='Выполнен').count()
    

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
            'in_pay_pickup': pay_method.in_pay_pickup,
            'description': pay_method.description
        })
    
    text_to_pay_cart = settings.text_to_pay_cart
    if not pay_methods_arr:

        if settings.only_pay_with_delivery:
            in_pay_delivery = False
        else:
            in_pay_delivery = True

        if not settings.only_pay_with_pickup:
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
            'name': text_to_pay_cart,
            'in_pay_delivery': True,
            'in_pay_pickup': True
        })


    

    subdomain_name = get_subdomain(request)
    try:
        subdomain = Subdomain.objects.filter(name=subdomain_name).first()
    except:
        subdomain = None

    
    
    pickup_areas_arr = []
    if subdomain:
        
        for pickup_area in pickup_areas:

            if pickup_area.city == subdomain:
                pickup_areas_arr.append({
                    'name': pickup_area.name
                })

    else:

        for pickup_area in pickup_areas:
            
            pickup_areas_arr.append({
                'name': pickup_area.name
            })
    
    if not pickup_areas_arr:
        pickup_areas_arr.append({
            'name': general_settings.address
        })

    hours = get_hours(request)

    active_balls = LoyaltyCardSettings.objects.get().active


    item = {
        
        'price_delivery': delivery_time_price()['price_delivery'],
        'free_delivery': delivery_time_price()['free_delivery'],
        'min_delivery': delivery_time_price()['min_delivery'],
        'zones_delivery': settings.zones_delivery,
        'hide_delivery_choosing': settings.hide_delivery_choosing,
        'first_delivery': settings.first_delivery,
        'discount_on_pickup': settings.discount_on_pickup,
        'summ_discount': settings.summ_discount,
        'check_order_status': settings.check_order_status,
        'active_balls': active_balls,
        
        
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

        
        try:

            loyal_cart_settings = LoyaltyCardSettings.objects.get()

            balls_min_summ = loyal_cart_settings.balls_min_summ
            exclude_combos = loyal_cart_settings.exclude_combos
            exclude_sales = loyal_cart_settings.exclude_sales

            loyal_cart = LoyaltyCard.objects.get(user=user)
            cart_summ = loyal_cart.summ
            cart_balls = loyal_cart.balls
            cart_status = loyal_cart.status()

            percent_down = cart_status.percent_down
            percent_down_pickup = cart_status.percent_down_pickup

            percent_pay = cart_status.percent_pay
            percent_pay_pickup = cart_status.percent_pay_pickup

            

            data = {
                'phone': user.phone,
                'cart_status': cart_status.name,
                'cart_summ': cart_summ,
                'cart_balls': cart_balls,
                'percent_down': percent_down,
                'percent_down_pickup': percent_down_pickup,
                'percent_pay': percent_pay,
                'percent_pay_pickup': percent_pay_pickup,
                'balls_min_summ': balls_min_summ,
                'exclude_combos': exclude_combos,
                'exclude_sales': exclude_sales,
            }

        except Exception as e:
            print(e)
            data = {
                'phone': user.phone,
                'cart_status': False,
                'cart_summ': 0,
                'cart_balls': 0,
                'percent_down': 0,
                'percent_down_pickup': 0,
                'percent_pay': 0,
                'percent_pay_pickup': 0,
                'balls_min_summ': 0,
                'exclude_combos': False,
                'exclude_sales': False,

            }
            return Response(data, status=status.HTTP_200_OK)

            
        return Response(data, status=status.HTTP_200_OK)
    except KeyError:
        return Response({'phone': 'error'}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({'phone': 'error'}, status=status.HTTP_200_OK)





from django.utils import timezone
from datetime import datetime, time
import pytz
from main.local_settings import TIME_ZONE

current_time = timezone.now()
# Определяем временную зону для сравнения
time_zone = pytz.timezone(TIME_ZONE)  # Замените 'Europe/Moscow' на вашу временную зону
# Конвертируем текущее время в нужную временную зону
current_time = current_time.astimezone(time_zone)


@api_view(['GET'])
def get_work_active(request, day):

    

    try:
        delivery_full = ShopSetup.objects.get().delivery_full
    except:
        delivery_full = False


    try:
        start_delivery = WorkDay.objects.get(day=day, active=True).start_delivery
        end_delivery = WorkDay.objects.get(day=day, active=True).end_delivery

        if end_delivery < start_delivery:

            end_delivery = '23:59:59'
            start_second_delivery = '00:00:00'
            end_second_delivery = WorkDay.objects.get(day=day, active=True).end_delivery


        else:
            start_delivery = WorkDay.objects.get(day=day, active=True).start_delivery
            end_delivery = WorkDay.objects.get(day=day, active=True).end_delivery

            start_second_delivery = None
            end_second_delivery = None

    except:

        start_delivery = ShopSetup.objects.get().start_delivery
        end_delivery = ShopSetup.objects.get().end_delivery
        


        if end_delivery < start_delivery:

            end_delivery = '23:59:59'
            start_second_delivery = '00:00:00'
            end_second_delivery = ShopSetup.objects.get().end_delivery
        else:

            start_second_delivery = None
            end_second_delivery = None


        

    day = datetime.now().weekday()
    

    # Проверяем, попадает ли текущее время в любой из интервалов доставки
    server_time = current_time.time()
    is_active = False  # По умолчанию считаем, что время не попадает в интервал

    try:
        if start_delivery <= server_time <= end_delivery:
            is_active = True
        elif start_second_delivery and end_second_delivery and start_second_delivery <= server_time <= end_second_delivery:
            is_active = True
            
    except:
        is_active = False

    work_day = False

    try: 
        WorkDay.objects.get(day=day, active=True).active
        work_day = True
    except:
        work_day = False
     
    try: 
        WorkDay.objects.get(day=day, active=False).active
        work_day = False
    except:
        work_day = True


    data = {
        'delivery_full': delivery_full,
        'start_delivery': start_delivery,
        'end_delivery': end_delivery,

        'start_second_delivery': start_second_delivery,
        'end_second_delivery': end_second_delivery,
        'day': day,
        'server_time': server_time,
        'is_active': is_active,
        'work_day': work_day
    }


    return Response(data, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_order_status(request, pk):
    order = Order.objects.get(id=pk)

    # print(order.STATUS_CLASS)

    if order.delivery_method == 'Самовывоз':
        status_list = [status_value for status_key, status_value in order.STATUS_CLASS_SELF_PICKUP if status_value != 'Готов к доставке' and status_value != 'Доставка' and status_value != 'Доставлен' and status_value != 'Отказ' and status_value != 'Выполнен']
    else:
        status_list = [status_value for status_key, status_value in order.STATUS_CLASS_DELIVERY if status_value != 'Готов к выдаче' and status_value != 'Доставка' and status_value != 'Доставлен' and status_value != 'Готов к доставке' and status_value != 'Отказ' and status_value != 'Выполнен']
    

    text_to_pay_cart = ShopSetup.objects.get().text_to_pay_cart

    data = {
        'status_list': status_list,
        'status': order.status,
        'pay_method': order.pay_method,
        'text_to_pay_cart': text_to_pay_cart,
        'paid': order.paid,
        'address': order.address,
        'delivery_method': order.delivery_method,
        'delivery_price': order.delivery_price,

    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def dop_items(request):
    dop_items = DopItems.objects.filter(required=True)
    serializer = DopItemsSerializer(dop_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
def check_promo(request):
    # Извлечение параметра 'promo' из строки запроса
    promo = request.query_params.get('promo')
    
    if not promo:
        return Response({'message': 'Необходимо указать промокод'}, status=status.HTTP_400_BAD_REQUEST)

    # Обработка промокода с помощью slugify
    try:
        slug = slugify(promo)
    except Exception as e:
        return Response({'message': 'Ошибка при обработке промокода', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    now = timezone.now()

    try:
        coupon = Coupon.objects.get(
            slug=slug,
            valid_from__lte=now,
            valid_to__gte=now,
            active=True
        )
    except Coupon.DoesNotExist:
        # Отправка сообщения в Telegram, если купон не найден
        coupon = None

    if coupon:
        data = {
            'message': 'Купон найден',
            'promo': coupon.code,
            'status': True,
            'coupon': coupon.discount,
            'type': coupon.promo_type
        }
    else:
        data = {
            'message': 'Купон не найден',
            'status': False,
            'coupon': 0
        }

    return Response(data, status=status.HTTP_200_OK)



# !!! Is admin !!! 
from sms.views import send_sms





from rest_framework import generics
class OrderViewList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderViewSerializer

    def get_queryset(self):
        # Получаем id заказа из URL-адреса
        order_id = self.kwargs.get('order_id')
        # Фильтруем OrderView по id заказа и текущему пользователю
        queryset = OrderView.objects.filter(order_id=order_id, user=self.request.user)
        return queryset


class OrderSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Получаем значение text_to_pay_cart из ShopSetup
        text_to_pay_cart = ShopSetup.objects.get().text_to_pay_cart

        # Проверяем способ оплаты и фильтруем соответственно
        queryset_paid = Order.objects.filter(pay_method=text_to_pay_cart, paid=True)
        queryset_unpaid = Order.objects.exclude(pay_method=text_to_pay_cart)

        result = queryset_paid | queryset_unpaid

        # Объединяем два queryset
        return result[:15]



    

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



