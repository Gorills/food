"""
Улучшенный модуль для генерации временных интервалов доставки
с корректной поддержкой часовых поясов и edge-cases
"""
from django.utils import timezone
from datetime import datetime, time, timedelta
import pytz
from shop.models import ShopSetup, WorkDay

# Словарь месяцев на русском языке
MONTHS = {
    1: 'Января', 2: 'Февраля', 3: 'Марта', 4: 'Апреля',
    5: 'Мая', 6: 'Июня', 7: 'Июля', 8: 'Августа',
    9: 'Сентября', 10: 'Октября', 11: 'Ноября', 12: 'Декабря'
}


def custom_round_time(dt, interval_minutes):
    """
    Округляет время до ближайшего интервала вверх.
    
    Args:
        dt: datetime или time объект
        interval_minutes: интервал в минутах (30 или 60)
    
    Returns:
        time объект с округленным временем
    """
    if isinstance(dt, time):
        dt = datetime.combine(datetime.today(), dt)
    elif isinstance(dt, str):
        dt = datetime.strptime(dt, "%H:%M")
    
    minutes = dt.minute
    
    # Округляем вверх до ближайшего интервала
    if minutes % interval_minutes != 0:
        rounded_minutes = ((minutes // interval_minutes) + 1) * interval_minutes
        
        # Если минуты >= 60, переходим на следующий час
        if rounded_minutes >= 60:
            dt += timedelta(hours=rounded_minutes // 60)
            rounded_minutes = rounded_minutes % 60
        
        dt = dt.replace(minute=rounded_minutes, second=0, microsecond=0)
    else:
        dt = dt.replace(second=0, microsecond=0)
    
    return dt.time()


def generate_time_intervals(start_dt, end_dt, interval_minutes):
    """
    Генерирует список временных интервалов между start_dt и end_dt.
    
    Args:
        start_dt: datetime начала
        end_dt: datetime окончания
        interval_minutes: интервал в минутах
    
    Returns:
        list: список строк вида "HH:MM - HH:MM"
    """
    time_list = []
    current_dt = start_dt
    
    # Генерируем интервалы до конечного времени
    while current_dt + timedelta(minutes=interval_minutes) <= end_dt:
        end_time = current_dt + timedelta(minutes=interval_minutes)
        time_str = f'{current_dt.strftime("%H:%M")} - {end_time.strftime("%H:%M")}'
        time_list.append(time_str)
        current_dt = end_time
    
    return time_list


def generate_now_intervals(current_dt, delay_minutes, start_delivery_dt, end_delivery_dt, interval_minutes):
    """
    Генерирует доступные интервалы с текущего момента с учетом задержки.
    
    Args:
        current_dt: текущее datetime (с учетом timezone)
        delay_minutes: задержка доставки в минутах
        start_delivery_dt: datetime начала доставки
        end_delivery_dt: datetime окончания доставки
        interval_minutes: интервал в минутах
    
    Returns:
        list: список доступных интервалов
    """
    # ВАЖНО: Сравниваем полные datetime, а не только time()
    # чтобы корректно работать с доставкой через полночь
    
    if current_dt < start_delivery_dt:
        # Рабочий день еще не начался, начинаем с начала рабочего времени
        start_time_dt = start_delivery_dt
    else:
        # Рабочий день уже идет, начинаем с текущего времени
        # Округляем текущее время вверх до ближайшего интервала
        rounded_time = custom_round_time(current_dt.time(), interval_minutes)
        start_time_dt = timezone.make_aware(datetime.combine(current_dt.date(), rounded_time))
        
        # Если после округления время меньше текущего, значит перешли на следующий час/день
        if rounded_time < current_dt.time():
            start_time_dt += timedelta(days=1)
        
        # Если start_time_dt получился раньше current_dt (из-за особенностей округления)
        # то устанавливаем следующий интервал
        if start_time_dt < current_dt:
            start_time_dt = current_dt.replace(second=0, microsecond=0)
            rounded_time = custom_round_time(start_time_dt.time(), interval_minutes)
            start_time_dt = timezone.make_aware(datetime.combine(start_time_dt.date(), rounded_time))
            if start_time_dt < current_dt:
                start_time_dt += timedelta(minutes=interval_minutes)
    
    # Добавляем задержку доставки
    start_time_dt += timedelta(minutes=delay_minutes)
    
    # Если после добавления задержки мы вышли за пределы рабочего времени
    if start_time_dt >= end_delivery_dt:
        return []
    
    # Генерируем интервалы
    return generate_time_intervals(start_time_dt, end_delivery_dt, interval_minutes)


def get_delivery_hours():
    """
    Получает временные интервалы доставки на ближайшие дни.
    Корректно работает с часовыми поясами и учитывает все edge-cases.
    
    Returns:
        list: список словарей с днями и доступными временами
              [{'while': 'Сегодня', 'times': ['Как можно скорее', '12:00 - 13:00', ...]}, ...]
    """
    # Получаем текущее время с учетом часового пояса
    current_time = timezone.localtime()
    
    # Получаем настройки доставки
    try:
        shop_setup = ShopSetup.objects.get()
    except ShopSetup.DoesNotExist:
        shop_setup = ShopSetup.objects.create()
    
    # Параметры доставки
    default_start = shop_setup.start_delivery if shop_setup.start_delivery else time(10, 0)
    default_end = shop_setup.end_delivery if shop_setup.end_delivery else time(22, 0)
    delay_minutes = shop_setup.delay if shop_setup.delay else 60  # delay уже в минутах!
    interval_minutes = shop_setup.interval if shop_setup.interval else 60
    delivery_full = shop_setup.delivery_full if hasattr(shop_setup, 'delivery_full') else False
    
    # Если круглосуточная доставка
    if delivery_full:
        default_start = time(0, 0)
        default_end = time(23, 59)
    
    # Получаем рабочие дни
    workdays = {wd.day: wd for wd in WorkDay.objects.all()}
    
    # Генерируем список дней
    days = []
    max_days = 7  # Показываем на неделю вперед
    
    for day_offset in range(max_days):
        target_date = current_time.date() + timedelta(days=day_offset)
        weekday = target_date.weekday()
        
        # Получаем рабочий день для этого дня недели
        workday = workdays.get(weekday)
        
        # Определяем время работы для этого дня
        if workday and workday.active:
            start_time = workday.start_delivery
            end_time = workday.end_delivery
        elif workday and not workday.active:
            # Если день неактивен, пропускаем его
            continue
        else:
            # Используем дефолтные настройки
            start_time = default_start
            end_time = default_end
        
        # Создаем timezone-aware datetime для начала и конца рабочего времени
        start_delivery_dt = timezone.make_aware(datetime.combine(target_date, start_time))
        end_delivery_dt = timezone.make_aware(datetime.combine(target_date, end_time))
        
        # Если конец доставки раньше начала (например, 22:00 - 02:00)
        if end_time < start_time:
            end_delivery_dt += timedelta(days=1)
        
        # Генерируем интервалы
        if day_offset == 0:
            # Для сегодняшнего дня проверяем, можно ли заказать на сегодня
            
            if current_time < start_delivery_dt:
                # Рабочий день еще не начался
                # ВАЖНО: Добавляем задержку к началу рабочего дня!
                # Если рабочий день с 10:00 и задержка 60 минут, 
                # то первый доступный интервал - 11:00
                start_with_delay = start_delivery_dt + timedelta(minutes=delay_minutes)
                
                # Проверяем, что после добавления задержки еще есть время для доставки
                if start_with_delay < end_delivery_dt:
                    time_intervals = generate_time_intervals(
                        start_with_delay,
                        end_delivery_dt,
                        interval_minutes
                    )
                    
                    if time_intervals:
                        # Добавляем "Как можно скорее" для сегодня
                        days.append({
                            'while': 'Сегодня',
                            'times': ['Как можно скорее'] + time_intervals
                        })
            else:
                # Рабочий день уже идет - генерируем от текущего времени
                time_intervals = generate_now_intervals(
                    current_time, 
                    delay_minutes, 
                    start_delivery_dt, 
                    end_delivery_dt, 
                    interval_minutes
                )
                
                # Добавляем "Сегодня" только если есть доступные интервалы
                if time_intervals:
                    days.append({
                        'while': 'Сегодня',
                        'times': ['Как можно скорее'] + time_intervals
                    })
        else:
            # Для будущих дней генерируем все интервалы
            # ВАЖНО: Также учитываем задержку для будущих дней
            start_with_delay = start_delivery_dt + timedelta(minutes=delay_minutes)
            
            # Проверяем что после задержки есть время для доставки
            if start_with_delay < end_delivery_dt:
                time_intervals = generate_time_intervals(
                    start_with_delay, 
                    end_delivery_dt, 
                    interval_minutes
                )
                
                # Формируем название дня
                day_num = target_date.day
                month_name = MONTHS[target_date.month]
                
                if day_offset == 1:
                    day_label = f'Завтра, {day_num} {month_name}'
                else:
                    day_label = f'{day_num} {month_name}'
                
                # Добавляем "Как можно скорее" для ВСЕХ дней
                if time_intervals:
                    days.append({
                        'while': day_label,
                        'times': ['Как можно скорее'] + time_intervals
                    })
    
    return days


def get_delivery_hours_api(request):
    """
    API endpoint для получения временных интервалов доставки.
    Wrapper для совместимости с существующим кодом.
    """
    return get_delivery_hours()

