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