from .models import Page
from orders.forms import OrderCreateForm
from shop.models import ShopSetup
from django.utils import timezone
from datetime import datetime, time
import pytz
from main.local_settings import TIME_ZONE

def get_work_active(request):

    try:
        current_time = timezone.now()

        # Определяем временную зону для сравнения
        time_zone = pytz.timezone(TIME_ZONE)  # Замените 'Europe/Moscow' на вашу временную зону

        # Конвертируем текущее время в нужную временную зону
        current_time = current_time.astimezone(time_zone)

        # Создаем объекты времени для начала и конца диапазона доставки
        start_time = time(ShopSetup.objects.get().start_delivery, 0)  # Начало доставки в 10:00
        end_time = time(ShopSetup.objects.get().end_delivery, 0)  # Конец доставки в 22:00

        # Создаем объекты datetime для сравнения времени
        current_datetime = datetime.combine(current_time.date(), current_time.time())
        start_datetime = datetime.combine(current_time.date(), start_time)
        end_datetime = datetime.combine(current_time.date(), end_time)

        # Проверяем, находится ли текущее время в диапазоне доставки
        if start_datetime <= current_datetime <= end_datetime:
            delivery_active = True
        else:
            delivery_active = False

    except:
        delivery_active = True
        start_time = time(ShopSetup.objects.get().start_delivery, 0)
        end_time = time(ShopSetup.objects.get().end_delivery, 0)

    print(current_time)
    return {
        'delivery_active': delivery_active,
        'start_time': start_time,
        'end_time': end_time
        
        }





def pages(request):
    return {'pages': Page.objects.filter(status=True)}

def odrer_form(request):
    return {'odrer_form': OrderCreateForm()}


from datetime import datetime, timedelta


def get_hours(request):

    try:
        start = ShopSetup.objects.get().start_delivery
        end = ShopSetup.objects.get().end_delivery
        delay = ShopSetup.objects.get().delay

        if ShopSetup.objects.get().delivery_full:
            start = 0
            end = 24
            

    except:
        start = 10
        end = 22
        delay = 2
    
    # Определяем задержку времени до доставки
    get_hour = int((datetime.now()+timedelta(hours=delay)).time().hour)

    hour_now = datetime.now().hour
    

    hour_list = []

    list_attach = []
    for i in range(end):
        if i >= start and i <= end:
            list_attach.append(i)
    list_attach.append(end)

    if hour_now in list_attach:
        for l in list_attach:
            item = str(l+delay) + ':00-' + str(l+delay) + ':30'
            item_two = str(l+delay) + ':30-' + str(l+delay+1) + ':00'

            if l >= hour_now and l <= end-delay-1:
                hour_list.append(item)
                hour_list.append(item_two)

    


    if hour_now < min(list_attach) and hour_now >= 0:
        hour_list = []
        count_two = 0
        for i in range(end):
            item = str(count_two+delay) + ':00-' + str(count_two+delay) + ':30'
            item_two = str(count_two+delay) + ':30-' + str(count_two+delay+1) + ':00'

            if count_two >= start and count_two + delay +1 <= end:
                hour_list.append(item)
                hour_list.append(item_two)
            count_two += 1



    hour_list_two = []
    count_two = 0
    for i in range(end):
        item = str(count_two+delay) + ':00-' + str(count_two+delay) + ':30'
        item_two = str(count_two+delay) + ':30-' + str(count_two+delay+1) + ':00'

        if count_two >= start and count_two + delay +1 <= end:
            hour_list_two.append(item)
            hour_list_two.append(item_two)
        count_two += 1

    try:
        get_sec = int((datetime.now() - datetime.strptime(request.session["code_date"], '%Y-%m-%d %H:%M:%S.%f')).total_seconds())
    except:
        get_sec = ''
    
    return {
        'get_hours': hour_list,
        'get_hours2': hour_list_two,
        'get_sec': get_sec
    }


def get_days(request):
    day_list = []
    count = 1
    get_day = datetime.now()
    for i in range(10):
        get_day = datetime.now() + timedelta(days=count)
        get_month = get_day.strftime("%b")
        if get_month == 'Nov':
            month = 'ноября'
        if get_month == 'Dec':
            month = 'декабря'
        if get_month == 'Jan':
            month = 'января'
        if get_month == 'Feb':
            month = 'февраля'
        if get_month == 'Mar':
            month = 'марта'
        if get_month == 'Apr':
            month = 'апреля'
        if get_month == 'May':
            month = 'мая'
        if get_month == 'Jun':
            month = 'июня'
        if get_month == 'Jul':
            month = 'июля'
        if get_month == 'Aug':
            month = 'августа'
        if get_month == 'Sep':
            month = 'сентября'
        if get_month == 'Oct':
            month = 'октября'
        if count == 1:
            day_str = 'Завтра, ' + str(get_day.day) + ' ' + month
        else:
            day_str = str(get_day.day) + ' ' + month
        
        day_list.append(day_str)

        count += 1
    
    return {'get_days': day_list}