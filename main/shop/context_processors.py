from django.utils import timezone  # Импортируем timezone из django.utils
import datetime
from main.local_settings import TIME_ZONE
import pytz
from .models import Category, Product, ShopSetup, PickupAreas, PayMethod, Combo, WorkDay

def categorys(request):
    return {'categorys': Category.objects.filter(status=True, show_in_site=True).order_by('sort_order')}

def categorys_top(request):
    return {'categorys_top': Category.objects.filter(status=True, top=True, show_in_site=True).order_by('sort_order')}

def combos(request):
    return {'combos': Combo.objects.all()}

# Показывать описания под товарами
def shop_setup(request):
    try:
        return {'shop_setup': ShopSetup.objects.get()}
    except:
        return {'shop_setup': ''}

def pickup_areas(request):
    try:
        return {'pickup_areas': PickupAreas.objects.all()}
    except:
        return {'pickup_areas': ''}

def pay_method(request):
    try:
        return {'pay_method': PayMethod.objects.all()}
    except:
        return {'pay_method': ''}

def pickup_address(request):
    try:
        return {'pickup_address': PickupAreas.objects.filter(show_to_contacts=True)}
    except:
        return {'pickup_address': None}

def cart_products(request):
    return {'cart_products': Product.objects.filter(in_cart=True, status=True)}


def delivery_today_available(request):
    # Текущее время с учетом временной зоны
    current_time = datetime.datetime.now(pytz.timezone(TIME_ZONE))
    
    # Получаем текущий день недели
    today_weekday = current_time.weekday()
    
    # Ищем рабочий день в базе данных
    workday = WorkDay.objects.filter(day=today_weekday, active=True).first()

    if workday:
        # Создаем start_delivery и end_delivery с учетом временной зоны
        start_delivery = current_time.replace(hour=workday.start_delivery.hour, minute=workday.start_delivery.minute, second=0, microsecond=0)
        end_delivery = current_time.replace(hour=workday.end_delivery.hour, minute=workday.end_delivery.minute, second=0, microsecond=0)
        
        # Проверяем, доступна ли доставка сегодня
        if start_delivery <= current_time <= end_delivery:
            return {'delivery_today_available': True}
    
    return {'delivery_today_available': False}
