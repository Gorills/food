
import re

import telepot

from setup.models import BaseSettings
from shop.models import ShopSetup






def send_message(telegram_bot, telegram_group, message):
    telegramBot = telepot.Bot(telegram_bot)
    telegramBot.sendMessage(telegram_group, message, parse_mode="Markdown")




def order_telegram(telegram_bot, telegram_group, order):
    pr = []
                    
    for item in order.items.all():
        if item.product:
            pr_name = item.product.name
            pr_quantity = item.quantity
            pr_price = str(item.price)
            pr_opt = item.options
                    
            pr_summ = (pr_quantity - item.free) * item.price

            pr_dict = {
                'Название': pr_name,
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
                'Состав':pr_sost,
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
                
                'Название':pr_name,
                'Категория': 'Конструктор блюд',
                'Состав':pr_sost,
                'Количество':pr_quantity,
                'Цена':pr_price,
                'Итого': str(pr_summ),
            })

    # res = re.sub(r"[#%!@*{}]", "\n", str(pr))
    # res = re.sub(r"[',]", "", res)
            
    # Преобразование списка товаров в текст с переносами строк
    res = "\n\n".join(["\n".join([f"{key}: {value}" for key, value in product.items()]) for product in pr])

    

    if order.address_comment:
        address_comment = "\n" + "*Комментарий к адресу*: " + str(order.address_comment) 
    else:
        address_comment = ''

    if order.order_conmment:
        order_conmment = "\n" + "*Комментарий к заказу*: " + str(order.order_conmment)
    else:
        order_conmment = ''

    time = order.time

    if order.discount:
        coupon_comment = "\n" + "*Купон/скидка*: " + str(order.discount) + "% ("+str(order.coupon.code)+")"
    else:
        coupon_comment = ''

    if order.bonuses_pay:
        bonuses_pay = f"\n*Оплачено баллами*: { order.bonuses_pay }"
    else:
        bonuses_pay = ''

    if order.entrance:
        entrance = "\n" + "*Подъезд*: " + str(order.entrance)
    else:
        entrance = ''

    if order.floor:
        floor = "\n" + "*Этаж*: " + str(order.floor)
    else:
        floor = ''

    if order.flat:
        flat = "\n" + "*Квартира*: " + str(order.flat)
    else:
        flat = ''

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
     
    
    if order.delivery_method == 'Доставка':
        
        message = "Заявка с сайта: " + "\n" + "*Номер заказа*: " +str(order.id) + "\n" + "*Имя*: " + str(order.name) + "\n" + "*Телефон*: " + str(phone) + "\n" + "*Время доставки*: " + str(time) + "\n" + "\n" + "*Адрес*: " + str(order.address) + entrance + floor + flat + address_comment + "\n" + "*Оплата*: " +str(order.pay_method) + not_pay + bonuses_pay + coupon_comment + "\n" + "*Доставка*: " +str(order.delivery_method) + "\n" + "*Стоимость доставки*: " +str(order.delivery_price) + order_conmment + "\n" + "\n" + "*Товары*: " + "\n" + str(res) + "\n\n" + "*Сумма заказа*: " + str(str(order.summ) + ' рублей')

    else:
        message = "Заявка с сайта: " + "\n" + "*Номер заказа*: " +str(order.id) + "\n" + "*Имя*: " + str(order.name) + "\n" + "*Телефон*: " + str(phone) + "\n" + "*Время самовывоза*: " + str(time) + "\n" + "*Адрес*: " + str(order.address) + "\n" + "*Оплата*: " +str(order.pay_method) + not_pay + bonuses_pay +  coupon_comment + "\n" + "*Доставка*: " +str(order.delivery_method) + order_conmment + "\n" + "\n" + "*Товары*: " + "\n" + str(res) + "\n\n" + "*Сумма заказа*: " + str(str(order.summ) + ' рублей')
    
    try:
        send_message(telegram_bot, telegram_group, message)
        
    except Exception as e:
        # print(e)
        pass
        