from .models import Page
from orders.forms import OrderCreateForm
from shop.models import ShopSetup


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
    except:
        start = 10
        end = 22
        delay = 2
    
    # Определяем задержку времени до доставки
    get_hour = int((datetime.now()+timedelta(hours=delay)).time().hour)

    hour_now = datetime.now().hour
    hour_list = []

    count = 0
    for i in range(11):
        item = str(get_hour+count) + ':00-' + str(get_hour+count) + ':30'
        item_two = str(get_hour+count) + ':30-' + str(get_hour+count+1) + ':00'
        # До какого времени + 30 минут возможна доставка
        if get_hour+count < end and hour_now >= start:
            hour_list.append(item)
            hour_list.append(item_two)

        count += 1

    # Если получаем пустой список, значит текущее время не попадает в доставку. Следовательно формируем список со всем возможным временем доставки
    if hour_list == []:
        for i in range(end-start-1):
            if i >= 1:
                item = str(get_hour+i) + ':00-' + str(get_hour+i) + ':30'
                item_two = str(get_hour+i) + ':30-' + str(get_hour+i+1) + ':00'

                if hour_now < start:
                    hour_list.append(item)
                    hour_list.append(item_two)

                count += 1



    hour_list_two = []
    count_two = 0
    for i in range(end):
        item = str(count_two+delay) + ':00-' + str(count_two+delay) + ':30'
        item_two = str(count_two+delay) + ':30-' + str(count_two+delay+1) + ':00'

        if count_two >= start and count_two + delay +1 <= end:
            hour_list_two.append(item)
            hour_list_two.append(item_two)
        count_two += 1

    
    return {
        'get_hours': hour_list,
        'get_hours2': hour_list_two,
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