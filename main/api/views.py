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
from shop.models import WorkDay
from subdomains.models import Subdomain



from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes




# Create your views here.
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
    orders = Order.objects.all().count()
    sales = Order.objects.all().aggregate(Sum('summ'))

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



from datetime import datetime, timedelta


def get_month_mame(month):
    if month == 'Nov':
        month = 'ноября'
    if month == 'Dec':
        month = 'декабря'
    if month == 'Jan':
        month = 'января'
    if month == 'Feb':
        month = 'февраля'
    if month == 'Mar':
        month = 'марта'
    if month == 'Apr':
        month = 'апреля'
    if month == 'May':
        month = 'мая'
    if month == 'Jun':
        month = 'июня'
    if month == 'Jul':
        month = 'июля'
    if month == 'Aug':
        month = 'августа'
    if month == 'Sep':
        month = 'сентября'
    if month == 'Oct':
        month = 'октября'
    
    return month


@api_view(['GET'])
def get_works_time(request):
    work_days = WorkDay.objects.all().order_by('day')

    # день недели
    current_day = datetime.now().weekday()
    # Число сегодня
    day_month = datetime.now().day
    
    # Час сейчас
    time_now = datetime.now().hour
    
    # Задержка на оформление заказа
    delay = ShopSetup.objects.get().delay
    delivery_full = ShopSetup.objects.get().delivery_full
    
    current_day = 4
    if work_days:
        res = {}
        count = 0
        for work_day in work_days:
            get_day = datetime.now() + timedelta(days=count)
            
            get_month = get_day.strftime("%b")
            month = get_month_mame(get_month)
            
            
            if work_day.day >= current_day:
                count += 1

                time_intervals = []

                if current_day == work_day.day:
                    day_name = 'Сегодня'
                    time_interval_two = f"Как можно скорее"
                    time_intervals.append(time_interval_two)
                elif current_day + 1 == work_day.day:
                    day_name = f'Завтра, {get_day.day} {month}'
                else:
                    day_name = f'{get_day.day}'


                if delivery_full:
                    start_delivery = 0
                    end_delivery = 23
                else:
                    start_delivery = int(work_day.start_delivery)
                    end_delivery = int(work_day.end_delivery)
                
                while start_delivery < end_delivery:
                    
                    if current_day == work_day.day:

                        if start_delivery > time_now:
                            time_interval_two = f"{start_delivery:02d}:00-{start_delivery + 1:02d}:00"
                            time_intervals.append(time_interval_two)
                            start_delivery += 1
                        else:
                            start_delivery += 1


                    else:
                        time_interval_two = f"{start_delivery:02d}:00-{start_delivery + 1:02d}:00"
                        time_intervals.append(time_interval_two)
                        start_delivery += 1

                if delivery_full:
                    time_interval_two = f"23:00-00:00"
                    time_intervals.append(time_interval_two)
                    start_delivery += 1

                res[day_name] = time_intervals

        return Response(res)
    else:
        return Response({"error": "No work days found"}, status=400)
