"""
Template filters для работы со временем
"""
from django import template
from datetime import time

register = template.Library()


@register.filter
def format_time_range(start_time, end_time):
    """
    Форматирует диапазон времени с учетом перехода через полночь.
    
    Использование в шаблоне:
    {{ shop_setup.start_delivery|format_time_range:shop_setup.end_delivery }}
    
    Вернет: "10:00 - 22:00" или "22:00 - 02:00 (следующего дня)"
    """
    if not start_time or not end_time:
        return ""
    
    start_str = start_time.strftime('%H:%M')
    end_str = end_time.strftime('%H:%M')
    
    if end_time < start_time:
        # Доставка через полночь
        return f"{start_str} - {end_str} (следующего дня)"
    else:
        return f"{start_str} - {end_str}"


@register.filter
def format_time(time_obj):
    """
    Форматирует время без секунд.
    
    Использование: {{ shop_setup.start_delivery|format_time }}
    Вернет: "10:00"
    """
    if not time_obj:
        return ""
    return time_obj.strftime('%H:%M')

