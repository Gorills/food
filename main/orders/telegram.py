
import re

import telepot

from setup.models import BaseSettings

try:
    token = BaseSettings.objects.get().telegram_bot
    my_id = BaseSettings.objects.get().telegram_group
except:
    token = ''
    my_id = ''


telegramBot = telepot.Bot(token)

def send_message(text):
    telegramBot.sendMessage(my_id, text, parse_mode="Markdown")




def order_telegram(order):
    pr = []
                    
    for item in order.items.all():
        pr_name = item.product.name
        pr_quantity = item.quantity
        pr_price = str(item.price)

        pr_summ = pr_quantity * item.price
        

        pr.append({
            
            'Название':pr_name,
            'Количество':pr_quantity,
            'Цена':pr_price,
            'Итого': str(pr_summ),
        })

    res = re.sub(r"[#%!@*{}]", "\n", str(pr))
    res = re.sub(r"[',]", "", res)

    if order.address_comment:
        address_comment = "\n" + "*Комментарий к адресу*: " + str(order.address_comment) 
    else:
        address_comment = ''

    if order.order_conmment:
        order_conmment = "\n" + "*Комментарий к заказу*: " + str(order.order_conmment)
    else:
        order_conmment = ''
    

    if order.delivery_method == 'Доставка':
        message = "Заявка с сайта: " + "\n" + "*Номер заказа*: " +str(order.id) + "\n" + "*Телефон*: " + str(order.phone) + "\n" + "*Адрес*: " + str(order.address) + "\n" + "*Подъезд*: " + str(order.entrance) + "\n" + "*Этаж*: " + str(order.floor) + "\n" + "*Квартира*: " + str(order.flat) + address_comment + "\n" + "*Оплата*: " +str(order.pay_method) + "\n" + "*Доставка*: " +str(order.delivery_method) + "\n" + "*Стоимость доставки*: " +str(order.delivery_price) + order_conmment + "\n" + "\n" + "*Товары*: " + "\n" + str(res) + "\n" + "*Итого*: " + str(str(order.summ) + ' рублей')

    else:
        message = "Заявка с сайта: " + "\n" + "*Номер заказа*: " +str(order.id) + "\n" + "*Телефон*: " + str(order.phone) + "\n" + "*Адрес*: " + str(order.address) + "\n" + "*Оплата*: " +str(order.pay_method) + "\n" + "*Доставка*: " +str(order.delivery_method) + order_conmment + "\n" + "\n" + "*Товары*: " + "\n" + str(res) + "\n" + "*Итого*: " + str(str(order.summ) + ' рублей')
    
    try:
        send_message(message)
    except Exception as e:
        print(e)
        