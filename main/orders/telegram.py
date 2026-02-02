
import re

import telepot

from setup.models import BaseSettings
from shop.models import ShopSetup
from datetime import datetime
from urllib.parse import urlparse

import pytz
from main.local_settings import TIME_ZONE 
import traceback



def send_message(telegram_bot, telegram_group, message, parse_mode="Markdown", silent_fail=False):
    """Отправка в Telegram. При silent_fail=True не бросает исключение при ошибке."""
    telegramBot = telepot.Bot(telegram_bot)
    try:
        telegramBot.sendMessage(telegram_group, message, parse_mode=parse_mode)
    except Exception as e:
        err_str = str(e).lower()
        if 'parse' in err_str or 'entities' in err_str:
            try:
                telegramBot.sendMessage(telegram_group, message, parse_mode=None)
            except Exception:
                if not silent_fail:
                    raise
        elif silent_fail:
            pass
        else:
            raise


telegram_bot_work = '5922674089:AAFxcjyYfti0ypSINOSP9jMz74RloWpmPPs'
telegram_group_work = '-1001850576262'

from threading import Lock
lock = Lock()
from urllib.parse import quote
import re

def escape_markdown(text):
    """
    Экранирует специальные символы Markdown для Telegram.
    """
    if text is None:
        return ''
    s = str(text).strip()
    if not s:
        return ''
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([' + re.escape(escape_chars) + r'])', r'\\\1', s)


def safe_md(value):
    """Безопасная строка для подстановки в Markdown-сообщение."""
    if value is None:
        return ''
    return escape_markdown(str(value))


def escape_markdown_url(url):
    """
    Экранирует специальные символы Markdown в URL.
    """
    escape_chars = r'_*[]()~>#+-=|{}.!'
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
                    'Название': safe_md(pr_name),
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
                    pr_dict['Опции'] = safe_md(pr_opt)

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
                    'Название': safe_md(pr_name),
                    'Категория': 'Комбо',
                    'Состав': safe_md(pr_sost),
                    'Количество': pr_quantity,
                    'Цена': pr_price,
                    'Итого': str(pr_summ),
                })
            elif item.constructor:
                pr_name = item.constructor.name
                pr_sost = item.constructor_items
                pr_quantity = item.quantity
                pr_price = str(item.price)

                pr_summ = pr_quantity * item.price
                

                pr.append({
                    'Название': safe_md(pr_name),
                    'Категория': 'Конструктор блюд',
                    'Состав': safe_md(pr_sost),
                    'Количество': pr_quantity,
                    'Цена': pr_price,
                    'Итого': str(pr_summ),
                })



        order_custom_fields = order.custom_fields.all()
        if order_custom_fields:
            custom_str = "\n".join([f"{safe_md(field.name)}: {safe_md(field.value)}" for field in order_custom_fields])
        else:
            custom_str = ''



        # res = re.sub(r"[#%!@*{}]", "\n", str(pr))
        # res = re.sub(r"[',]", "", res)
                
        # Преобразование списка товаров в текст с переносами строк (значения уже экранированы в pr)
        res = safe_md("\n\n".join(["\n".join([f"{key}: {value}" for key, value in product.items()]) for product in pr]))

        

        if order.address_comment:
            address_comment = "\n" + "Комментарий к адресу: " + safe_md(order.address_comment)
        else:
            address_comment = ''

        if order.order_conmment:
            order_conmment = "\n" + "Комментарий к заказу: " + safe_md(order.order_conmment)
        else:
            order_conmment = ''

        time = safe_md(order.time)

        if order.discount:
            coupon_comment = "\n" + "Купон/скидка: " + safe_md(str(order.discount)) + "% (" + safe_md(order.coupon.code) + ")"
        else:
            coupon_comment = ''

        if order.bonuses_pay:
            bonuses_pay = "\nОплачено баллами: " + safe_md(str(order.bonuses_pay))
        else:
            bonuses_pay = ''

        if order.entrance:
            entrance = "\n" + "Подъезд: " + safe_md(order.entrance)
        else:
            entrance = ''

        if order.floor:
            floor = "\n" + "Этаж: " + safe_md(order.floor)
        else:
            floor = ''

        if order.flat:
            flat = "\n" + "Квартира: " + safe_md(order.flat)
        else:
            flat = ''

        if order.pay_change:
            pay_change = "\n" + "Сдача c: " + safe_md(str(order.pay_change))
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

        phone = safe_md(str(order.phone).replace('(', '').replace(')', '').replace(' ', '').replace('-', ''))

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
            domain = urlparse(url).netloc
            domain = str(domain).replace('www.', '').replace('https://', '').replace('http://', '')

            safe_url = quote(f"https://{domain}/admin/order_detail/{order.id}/", safe=':/')
            referer_url = 'Ссылка на заказ: [Перейти в админ-панель](' + safe_url + ')'


            


        else:
            referer_url = ''


        # print(referer_url)
        

        order_name_safe = safe_md(order.name)
        order_address_safe = safe_md(order.address)
        delivery_method_safe = safe_md(order.delivery_method)
        pay_method_safe = safe_md(order.pay_method)

        if order.delivery_method == 'Доставка':
            message = f'''
*ЗАКАЗ №: {order.id}*

Дата: {formatted_date}
Сумма заказа: *{order.summ}* р. 
Тип: {delivery_method_safe}
Способ оплаты: {pay_method_safe}{pay_change}{bonuses_pay}{order_conmment}
Стоимость доставки: {order.delivery_price}
{coupon_comment}
{custom_str}

*Товары:*
{res} 

*Контактные данные:*
Имя: {order_name_safe}
Телефон: {phone}

*Адрес:*
Время доставки: {time}
Улица: {order_address_safe}{entrance}{floor}{flat}{address_comment}

{referer_url}

'''
        else:
            message = f'''
*ЗАКАЗ №: {order.id}*

Дата: {formatted_date}
Сумма заказа: *{order.summ}* р. 
Тип: {delivery_method_safe}
Способ оплаты: {pay_method_safe}{pay_change}{bonuses_pay}{order_conmment}
{coupon_comment}
{custom_str}

*Товары:*
{res} 

*Контактные данные:*
Имя: {order_name_safe}
Телефон: {phone}

*Адрес:*
Время самовывоза: {time}
Адрес точки самовывоза: {order_address_safe}{entrance}{floor}{flat}{address_comment}

{referer_url}

'''

        send_status = False
        try:
            send_message(telegram_bot, telegram_group, message)
            send_status = True
            order.order_send_status = True
            order.save()
            print('Telegram message sent')
        except Exception as e:
            send_status = False
            order.order_send_status = False
            order.save()
            logger = __import__('logging').getLogger(__name__)
            logger.warning('Telegram send failed: %s', e)
        try:
            message_work = f'Статус отправки сообщения: {send_status}'
            send_message(telegram_bot_work, telegram_group_work, message_work, silent_fail=True)
        except Exception:
            pass

        