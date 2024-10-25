from django.utils import timezone
from datetime import datetime, time, timedelta
import pytz
from shop.models import ShopSetup, WorkDay
from main.local_settings import TIME_ZONE

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
    12: 'Декабря'
}

def custom_round_time(current_time, interval):
    current_datetime = datetime.strptime(current_time, "%H:%M") if isinstance(current_time, str) else current_time
    minutes = current_datetime.minute

    # Округление в большую сторону, если минуты не кратны интервалу
    if minutes % interval != 0:
        rounded_minutes = minutes + interval - (minutes % interval)
        if interval == 60 and rounded_minutes == 60:
            current_datetime += timedelta(hours=1)
            rounded_minutes = 0
        current_datetime = current_datetime.replace(minute=rounded_minutes % 60, hour=(current_datetime.hour + rounded_minutes // 60) % 24)

    rounded_time = current_datetime.time()
    return rounded_time

def generate_time_intervals(start_datetime, end_datetime, interval, delay):
    time_list = []
    current_time_while = start_datetime + timedelta(minutes=delay)

    while current_time_while < end_datetime:
        end_time = current_time_while + timedelta(minutes=interval)
        time_list.append(f'{current_time_while.time().strftime("%H:%M")} - {end_time.time().strftime("%H:%M")}')
        current_time_while = end_time
    return time_list

def generate_now_intervals(current_time, delay, start_datetime, end_datetime, interval, count=0):
    current_datetime = current_time.time()

    # Начнем с текущего времени или старта рабочего дня в зависимости от того, что больше
    if start_datetime.time() > current_datetime:
        now_start_time = start_datetime
    else:
        now_start_time = datetime.combine(current_time.date(), custom_round_time(current_datetime.strftime("%H:%M"), interval))

    now_start_time += timedelta(minutes=delay)
    time_intervals_now = []
    current_time_while = now_start_time

    while current_time_while <= end_datetime:
        end_time = current_time_while + timedelta(minutes=interval)
        start_time_str = current_time_while.time().strftime('%H:%M')
        end_time_str = end_time.time().strftime('%H:%M')

        if interval == 60:
            if current_time_while >= end_datetime:
                time_intervals_now.append(f'До {start_time_str}')
            else:
                time_intervals_now.append(f'{start_time_str} - {end_time_str}')
        else:
            if current_time_while >= end_datetime:
                time_intervals_now.append(f'До {start_time_str}')
            else:
                time_intervals_now.append(f'{start_time_str} - {end_time_str}')

        current_time_while = end_time

    return time_intervals_now

def get_hours(request):
    workdays = WorkDay.objects.filter(active=True)
    current_time = timezone.now().astimezone(pytz.timezone(TIME_ZONE))

    try:
        shop_setup = ShopSetup.objects.get()
    except ShopSetup.DoesNotExist:
        shop_setup = ShopSetup.objects.create()

    start = shop_setup.start_delivery
    end = shop_setup.end_delivery
    delay = shop_setup.delay
    interval = shop_setup.interval
    delivery_full = shop_setup.delivery_full

    if delivery_full:
        start = time(0, 0)
        end = time(23, 59)

    start_datetime = datetime.combine(datetime.today(), start)
    end_datetime = datetime.combine(datetime.today(), end)

    # Если время заканчивается на следующий день
    next_day_delivery = False
    if end < start:
        end_datetime += timedelta(days=1)
        next_day_delivery = True
    
    count = 0
    days = []
    now_date = current_time

    while count < 24:
        mod_date = now_date + timedelta(days=count)
        day_count_now = mod_date.weekday()
        day_now = mod_date.day
        month_now = mod_date.month

        workday = workdays.filter(day=day_count_now).first()

        # Если рабочего дня нет вообще, используем время из ShopSetup
        if not workday:
            start_delivery = datetime.combine(mod_date, start)
            end_delivery = datetime.combine(mod_date, end)
            if next_day_delivery:
                end_delivery += timedelta(days=1)

            time_intervals_now = generate_now_intervals(current_time, delay, start_delivery, end_delivery, interval, count)
            time_intervals = generate_time_intervals(start_delivery, end_delivery, interval, delay)

            if count == 0 and time_intervals_now:
                days.append({'while': 'Сегодня', 'times': ['Как можно скорее'] + time_intervals_now})
            elif count == 1:
                if next_day_delivery:
                    days.append({'while': f'Завтра, {day_now} {months[month_now]}', 'times': time_intervals})
                else:
                    days.append({'while': f'Завтра, {day_now} {months[month_now]}', 'times': ['Как можно скорее'] + time_intervals})
            else:
                days.append({'while': f'{day_now} {months[month_now]}', 'times': time_intervals})
            
            count += 1
            continue

        if workday and workday.active:
            start_delivery = datetime.combine(mod_date, workday.start_delivery if workday else start)
            end_delivery = datetime.combine(mod_date, workday.end_delivery if workday else end)
            if workday.end_delivery < workday.start_delivery:
                end_delivery += timedelta(days=1)
                next_day_delivery = True
            
            time_intervals_now = generate_now_intervals(current_time, delay, start_delivery, end_delivery, interval, count)
            time_intervals = generate_time_intervals(start_delivery, end_delivery, interval, delay)

            if count == 0 and workday and workday.active and time_intervals_now:
                days.append({'while': 'Сегодня', 'times': ['Как можно скорее'] + time_intervals_now})
            elif count == 1 and workday and workday.active:
                if next_day_delivery:
                    days.append({'while': f'Завтра, {day_now} {months[month_now]}', 'times': time_intervals})
                else:
                    days.append({'while': f'Завтра, {day_now} {months[month_now]}', 'times': ['Как можно скорее'] + time_intervals})
            else:
                days.append({'while': f'{day_now} {months[month_now]}', 'times': time_intervals})

        count += 1

    return days
