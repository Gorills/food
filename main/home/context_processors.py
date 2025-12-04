from .models import Page
from orders.forms import OrderCreateForm
from shop.models import ShopSetup, WorkDay
from django.utils import timezone
from datetime import datetime, time
import pytz
from main.local_settings import TIME_ZONE


current_time = timezone.now()
# Определяем временную зону для сравнения
time_zone = pytz.timezone(TIME_ZONE)  # Замените 'Europe/Moscow' на вашу временную зону
# Конвертируем текущее время в нужную временную зону
current_time = current_time.astimezone(time_zone)

try:
    delivery_full = ShopSetup.objects.get().delivery_full
except:
    delivery_full = False

# current_time = datetime.combine(current_time.date(), datetime.strptime('22:05', "%H:%M").time())
# print(current_time)



def get_work_active(request):
    

    if not delivery_full:
        try:
            try:
                workday = WorkDay.objects.get(day=current_time.weekday())
                
            except:
                workday = None
                
            

            # Создаем объекты времени для начала и конца диапазона доставки
            start_time = ShopSetup.objects.get().start_delivery  # Начало доставки в 10:00
            end_time = ShopSetup.objects.get().end_delivery  # Конец доставки в 22:00

            # Создаем объекты datetime для сравнения времени
            current_datetime = datetime.combine(current_time.date(), current_time.time())

            if workday:
                start_datetime = datetime.combine(current_time.date(), workday.start_delivery)
                end_datetime = datetime.combine(current_time.date(), workday.end_delivery)
                workday_active = workday.active
            else:
                start_datetime = datetime.combine(current_time.date(), start_time)
                end_datetime = datetime.combine(current_time.date(), end_time)
                workday_active = True

            
            if start_datetime < end_datetime:
                # Проверяем, находится ли текущее время в диапазоне доставки
                if start_datetime <= current_datetime <= end_datetime:
                    delivery_active = True
                else:
                    delivery_active = False

            else:
                if start_datetime <= current_datetime or current_datetime <= end_datetime:
                    delivery_active = True
                else:
                    delivery_active = False

        except Exception as e:
            
            delivery_active = True
            start_time = time(int('10'), 0)
            end_time = time(int('21'), 0)
            workday_active = True

            start_datetime = datetime.combine(current_time.date(), start_time)
            end_datetime = datetime.combine(current_time.date(), end_time)

    else:
        delivery_active = True
        start_time = time(int('0'), 0)
        end_time = time(int('0'), 0)
        workday_active = True

        start_datetime = datetime.combine(current_time.date(), start_time)
        end_datetime = datetime.combine(current_time.date(), end_time)

    
    
    return {
        'delivery_active': delivery_active,
        'workday_active': workday_active,
        'start_time': start_datetime.time().strftime('%H:%M'),
        'end_time': end_datetime.time().strftime('%H:%M')
        
        }





def pages(request):
    return {'pages': Page.objects.filter(status=True)}

def odrer_form(request):
    return {'odrer_form': OrderCreateForm()}


from datetime import datetime, timedelta

# Импортируем улучшенную версию для генерации временных интервалов
from api.delivery_time import get_delivery_hours as get_delivery_hours_improved

def custom_round_time(current_time, interval):
    current_datetime = datetime.strptime(current_time, "%H:%M")
    minutes = current_datetime.minute

    # Округление в большую сторону, если минуты не кратны интервалу
    if minutes % interval != 0:
        try:
            rounded_minutes = minutes + interval - (minutes % interval)
        except ValueError:
            rounded_minutes = minutes
        # Учет промежутка в час при интервале 60 минут
        if interval == 60 and rounded_minutes == 60:
            current_datetime += timedelta(hours=1)
            rounded_minutes = 0
        current_datetime = current_datetime.replace(minute=rounded_minutes % 60, hour=(current_datetime.hour + rounded_minutes // 60) % 24)

    rounded_time = current_datetime.time()

    

    return rounded_time


def generate_time_intervals(start_datetime, end_datetime, interval):
    time_list = []
    current_time_while = start_datetime
    
    while current_time_while < end_datetime:
        end_time = current_time_while + timedelta(minutes=interval)
        end_time_str = end_time.time().strftime('%H:%M')
        if interval == 60:
            start_time_str = current_time_while.time().strftime('%H:%M')
            time_list.append(f'{start_time_str} - {end_time_str}')
        else:
            time_list.append(f'{current_time_while.time().strftime("%H:%M")} - {end_time_str}')
        current_time_while = end_time
    return time_list


def generate_now_intervals(current_time, delay, start_datetime, end_datetime, interval):
    current_datetime = datetime.strptime(current_time.time().strftime('%H:%M'), "%H:%M").time()


    if start_datetime.time() > current_datetime:
        now_start_time = start_datetime
    else:
        now_start_time = datetime.combine(current_time.date(), custom_round_time(current_time.time().strftime('%H:%M'), interval))
    
    now_start_time += timedelta(hours=delay)
    # print(custom_round_time(current_time.time().strftime('%H:%M'), interval), now_start_time)

    time_intervals_now = []
    current_time_while = now_start_time


    while current_time_while <= end_datetime:
        end_time = current_time_while + timedelta(minutes=interval)
        end_time_str = end_time.time().strftime('%H:%M')

        if interval == 60:
            start_time_str = current_time_while.time().strftime('%H:%M')

            if current_time_while >= end_datetime:

                

                time_intervals_now.append(f'До {start_time_str}')
            else:
                time_intervals_now.append(f'{start_time_str} - {end_time_str}')
        else:

            start_time_str = current_time_while.time().strftime('%H:%M')
            if current_time_while >= end_datetime:

                

                time_intervals_now.append(f'До {start_time_str}')
            else:
                time_intervals_now.append(f'{start_time_str} - {end_time_str}')
            

            # time_intervals_now.append(f'{current_time_while.time().strftime("%H:%M")} - {end_time_str}')

        current_time_while = end_time

        

    return time_intervals_now



def generate_dop_intervals(start_datetime, end_datetime, interval):
    dop_time_list = []
    
    if end_datetime < start_datetime:
        dop_start_date = datetime.combine(end_datetime.date(), time(0, 0, 0)) + timedelta(days=1)
        current_time_while = dop_start_date

            
        while current_time_while < end_datetime + timedelta(days=1):
            end_time = current_time_while + timedelta(minutes=interval)
            end_time_str = end_time.time().strftime('%H:%M')
            if interval == 60:
                start_time_str = current_time_while.time().strftime('%H:%M')
                dop_time_list.append(f'{start_time_str} - {end_time_str}')
            else:
                dop_time_list.append(f"{current_time_while.time().strftime('%H:%M')} - {end_time_str}")
            current_time_while = end_time
        end_datetime = datetime.combine(end_datetime.date(), time(23, 59, 59))

    return dop_time_list


def get_hours(request):
    """
    Получает временные интервалы доставки для отображения в шаблонах.
    ОБНОВЛЕНО: теперь использует улучшенную версию с корректной работой timezone.
    """
    # Используем улучшенную версию
    return get_delivery_hours_improved()
    
    # Старый код закомментирован (оставлен для справки)
    """
    workdays = WorkDay.objects.all()


    days = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье',
    }

    months = {
        1: 'Января',
        2: 'Февраля',
        3: 'Марта',
        4: 'Апреля',
        5: 'Мая',
        6: 'Июня',
        7: 'Июля',
        8: 'Августа',
        9: 'Сентября',
        10: 'Октября',
        11: 'Ноября',
        12: 'Декабря',
    }

    
    now_date = datetime.now()

    try:
        shop_setup = ShopSetup.objects.get()
    except:
        shop_setup = ShopSetup.objects.create()
        

    start = shop_setup.start_delivery
    end = shop_setup.end_delivery
    delay = shop_setup.delay
    interval = shop_setup.interval

    

    if delivery_full:
        start = time(0, 0)
        end = time(23, 59)
        

    start_datetime = datetime.combine(datetime.today(), start)
    end_datetime = datetime.combine(datetime.today(), end)

    # Добавляем задержку, если она есть
    if ShopSetup.objects.get().delivery_full:
        start_datetime += timedelta(hours=0)
    else:
        start_datetime += timedelta(hours=delay)

    

    count = 0
    days = []
     

    while count < 6:
        mod_date = now_date + timedelta(days=count)

        day_count_now = mod_date.weekday()
        day_now = mod_date.day
        month_now = mod_date.month  


        try:
            workday = WorkDay.objects.get(day=day_count_now)
        except:
            workday = None
        
        if workday:

            if workday.active:
                start_delivery = datetime.combine(datetime.today(), workday.start_delivery)
                end_delivery = datetime.combine(datetime.today(), workday.end_delivery)
                
                

                if end_delivery < start_delivery:        
                    end_delivery_fix = datetime.combine(end_datetime.date(), time(23, 59, 59))
                else:
                    end_delivery_fix = end_delivery

                start_delivery += timedelta(hours=delay)
                time_intervals_now = generate_now_intervals(current_time, delay, start_delivery, end_delivery_fix, interval)
                time_intervals = generate_time_intervals(start_delivery, end_delivery_fix, interval)

                if time_intervals_now == []:
                    dop_time_list = []

                if count == 0:
                    if time_intervals_now != []:
                        days.append({'while':'Сегодня', 'times': ['Как можно скорее'] + time_intervals_now})

                elif count == 1:
                   
                    days.append({'while':f'Завтра, {day_now} {months[month_now]}', 'times': ['Как можно скорее'] + dop_time_list + time_intervals})

                else:
                    days.append({'while':f'{day_now} {months[month_now]}', 'times': dop_time_list + time_intervals})
                
                dop_time_list = generate_dop_intervals(start_delivery, end_delivery, interval)

            else:
                dop_time_list = []

            # print(day_count_now)
        else:

            
            if end_datetime < start_datetime:        
                end_datetime_fix = datetime.combine(end_datetime.date(), time(23, 59, 59))
            else:
                end_datetime_fix = end_datetime

            time_intervals_now = generate_now_intervals(current_time, delay, start_datetime, end_datetime_fix, interval)
            time_intervals = generate_time_intervals(start_datetime, end_datetime_fix, interval)
            if time_intervals_now == []:
                dop_time_list = []
            if count == 0:
                if time_intervals_now != []:
                    days.append({'while':'Сегодня', 'times': ['Как можно скорее'] + time_intervals_now})
                
            elif count == 1:
                days.append({'while':f'Завтра, {day_now} {months[month_now]}', 'times': ['Как можно скорее'] +  dop_time_list + time_intervals})
                
            else:
                days.append({'while':f'{day_now} {months[month_now]}', 'times': ['Как можно скорее'] + dop_time_list + time_intervals})

            dop_time_list = generate_dop_intervals(start_datetime, end_datetime, interval)

        count += 1

    # print(days)



    try:
        get_sec = int((datetime.now() - datetime.strptime(request.session["code_date"], '%Y-%m-%d %H:%M:%S.%f')).total_seconds())
    except:
        get_sec = ''

    return {
        
        'get_days': days,
        'get_sec': get_sec
    }
    """





def image_size_get(request):

    image_size = f'{ShopSetup.objects.get().min_width}x{ShopSetup.objects.get().min_height}'

    return {'image_size': image_size}