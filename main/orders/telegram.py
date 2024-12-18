
import re

import telepot

from setup.models import BaseSettings
from shop.models import ShopSetup
from datetime import datetime

from datetime import datetime
import pytz
from main.local_settings import TIME_ZONE 




def send_message(telegram_bot, telegram_group, message):
    telegramBot = telepot.Bot(telegram_bot)
    telegramBot.sendMessage(telegram_group, message, parse_mode="Markdown")


telegram_bot_work = '5922674089:AAFxcjyYfti0ypSINOSP9jMz74RloWpmPPs'
telegram_group_work = '-1001850576262'

from threading import Lock
lock = Lock()


def escape_markdown(text):
    """
    Экранирует специальные символы Markdown.
    """
    import re
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"[{re.escape(escape_chars)}]", r"\\\g<0>", text)


def escape_markdown_url(url):
    """
    Экранирует символы Markdown в URL.
    """
    import re
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"[{re.escape(escape_chars)}]", r"\\\g<0>", url)



def order_telegram(telegram_bot, telegram_group, order, request=None):

   

    with lock:
        if order.order_send_status:
            return
        
        pr = []
        
        # print(order)
        
        for item in order.items.all():
            
            if item.product:
                pr_name = item.product.name
                pr_quantity = item.quantity
                pr_price = str(item.price)
                pr_opt = item.options
                        
                pr_summ = (pr_quantity - item.free) * item.price

                pr_dict = {
                    'Название': pr_name.replace('*', ''),
                    'Количество': pr_quantity,
                    'Цена': pr_price,
                    'Итого': str(pr_summ),
                }
                try:
                    pr_dict['Категория'] = item.product.parent.name
                except:
                    pass

                if item.product.related:
                    pr_dict['Категория'] = 'Сопутствующий товар'

                    
                # Далее переместим 'Категория' после 'Название', если оно было добавлено
                if 'Категория' in pr_dict:
                    pr_dict = {key: pr_dict[key] for key in ['Название', 'Категория', 'Количество', 'Цена', 'Итого'] if key in pr_dict}

                if pr_opt is not None:
                    pr_dict['Опции'] = pr_opt

                pr_weight = item.weight
                if pr_weight is not None:
                    pr_dict['Вес'] = pr_weight
                
                pr.append(pr_dict)
                
            elif item.combo:
                pr_name = item.combo.name
                pr_sost = item.combo_items
                pr_quantity = item.quantity
                pr_price = str(item.price)

                pr_summ = pr_quantity * item.price
                

                pr.append({
                    
                    'Название':pr_name,
                    'Категория': 'Комбо',
                    'Состав':pr_sost.replace('*', ''),
                    'Количество':pr_quantity,
                    'Цена':pr_price,
                    'Итого': str(pr_summ),
                })
            elif item.constructor:
                pr_name = item.constructor.name
                pr_sost = item.constructor_items
                pr_quantity = item.quantity
                pr_price = str(item.price)

                pr_summ = pr_quantity * item.price
                

                pr.append({
                    
                    'Название':pr_name.replace('*', ''),
                    'Категория': 'Конструктор блюд',
                    'Состав':pr_sost.replace('*', ''),
                    'Количество':pr_quantity,
                    'Цена':pr_price,
                    'Итого': str(pr_summ),
                })



        order_custom_fields = order.custom_fields.all()
        if order_custom_fields:
            custom_str = "\n".join([f"{field.name}: {field.value}" for field in order_custom_fields])
        else:
            custom_str = ''



        # res = re.sub(r"[#%!@*{}]", "\n", str(pr))
        # res = re.sub(r"[',]", "", res)
                
        # Преобразование списка товаров в текст с переносами строк
        res = "\n\n".join(["\n".join([f"{key}: {value}" for key, value in product.items()]) for product in pr])

        

        if order.address_comment:
            address_comment = "\n" + "Комментарий к адресу: " + str(order.address_comment) 
        else:
            address_comment = ''

        if order.order_conmment:
            order_conmment = "\n" + "Комментарий к заказу: " + str(order.order_conmment)
        else:
            order_conmment = ''

        time = order.time

        if order.discount:
            coupon_comment = "\n" + "Купон/скидка: " + str(order.discount) + "% ("+str(order.coupon.code)+")"
        else:
            coupon_comment = ''

        if order.bonuses_pay:
            bonuses_pay = f"\nОплачено баллами: { order.bonuses_pay }"
        else:
            bonuses_pay = ''

        if order.entrance:
            entrance = "\n" + "Подъезд: " + str(order.entrance)
        else:
            entrance = ''

        if order.floor:
            floor = "\n" + "Этаж: " + str(order.floor)
        else:
            floor = ''

        if order.flat:
            flat = "\n" + "Квартира: " + str(order.flat)
        else:
            flat = ''

        if order.pay_change:
            pay_change = "\n" + "Сдача c: " + str(order.pay_change)
        else:
            pay_change = ''

        if order.pay_method == 'Оплата картой на сайте':
            if ShopSetup.objects.get().info_to_order_anyway == True:
                
                if order.paid == True:
                    not_pay = "\n" + "*Статус оплаты*: *ОПЛАЧЕН*"
                else:
                    not_pay = "\n" + "*Статус оплаты*: *НЕ ОПЛАЧЕН! ПРЕДВАРИТЕЛЬНОЕ ОПОВЕЩЕНИЕ О ЗАКАЗЕ*"
            else:
                not_pay = ''
        else:
            not_pay = ""

        phone = order.phone
        phone = str(phone).replace('(', '').replace(')', '').replace(' ', '').replace('-', '')

        # Предполагается, что order.created уже является объектом datetime.datetime
        order_created_utc = order.created

        # Определите нужный вам часовой пояс
        desired_timezone = pytz.timezone(TIME_ZONE)

        # Преобразуйте время из UTC в выбранный часовой пояс
        order_created_local = order_created_utc.replace(tzinfo=pytz.utc).astimezone(desired_timezone)

        # Форматирование даты в нужный вам формат
        formatted_date = order_created_local.strftime("%d.%m.%Y %H:%M:%S")

        if request:
            url = request.META.get('HTTP_REFERER', '').replace('http://', 'https://')

            referer_url = f'Ссылка на заказ: [Перейти в админ-панель сайта]({url}admin/order_detail/{order.id}/)'

        else:
            referer_url = ''

        print("referer_url", referer_url)

        if order.delivery_method == 'Доставка':
            message = f'''
*ЗАКАЗ №: {order.id}*

Дата: {formatted_date}
Сумма заказа: *{order.summ}* р. 
Тип: {order.delivery_method}
Способ оплаты: {order.pay_method}{pay_change}{bonuses_pay}{order_conmment}
Стоимость доставки: {order.delivery_price}
{coupon_comment}
{custom_str}

*Товары:*
{str(res)} 

*Контактные данные:*
Имя: {order.name}
Телефон: {phone}

*Адрес:*
Время доставки: {time}
Улица: {order.address}{entrance}{floor}{flat}{address_comment}

{referer_url}

'''
        else:
            message = f'''
*ЗАКАЗ №: {order.id}*

Дата: {formatted_date}
Сумма заказа: *{order.summ}* р. 
Тип: {order.delivery_method}
Способ оплаты: {order.pay_method}{pay_change}{bonuses_pay}{order_conmment}
{coupon_comment}
{custom_str}

*Товары:*
{str(res)} 

*Контактные данные:*
Имя: {order.name}
Телефон: {phone}

*Адрес:*
Время самовывоза: {time}
Адрес точки самовывоза: {order.address}{entrance}{floor}{flat}{address_comment}

{referer_url}

'''

        try:
            send_message(telegram_bot, telegram_group, message)
            send_status = True
            order.order_send_status = True
            order.save()

            message_work = f'Статус отправки сообщения: {send_status}'
            send_message(telegram_bot_work, telegram_group_work, message_work)
            print('Telegram message sent')
            

        except Exception as e:
            send_message(telegram_bot, telegram_group, e)

        