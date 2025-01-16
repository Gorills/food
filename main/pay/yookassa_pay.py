from decimal import Decimal
from django.shortcuts import render

from .models import PaymentSet, Yookassa
from shop.models import Product, Combo, ProductOption
from subdomains.utilites import get_protocol
from setup.models import ThemeSettings, BaseSettings
# Create your views here.
from yookassa import Configuration, Payment

try:
    Configuration.account_id = Yookassa.objects.get().shop_id
    Configuration.secret_key = Yookassa.objects.get().key
except:
    Configuration.account_id = ''
    Configuration.secret_key = ''

try:
    telegram_bot = BaseSettings.objects.get().telegram_bot
    telegram_group = BaseSettings.objects.get().telegram_group
except Exception as e:
    
    telegram_bot = ''
    telegram_group = ''

from orders.telegram import order_telegram, send_message



from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
import uuid
from yookassa import Payment

def format_price(price):
    # Округляем до двух знаков после запятой, как это требуется платежной системой
    return str(Decimal(price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
def create_payment(order, cart, request):

    try:
        path = f'{get_protocol(request)}://' + request.META['HTTP_HOST']
        
        items = []
        
        phone = order.phone
        digits_only = ''.join(char for char in phone if char.isdigit())
        
        sale_percent = order.sale_percent
        
        total_items_sum = Decimal(0)
        
        # Формируем список товаров
        for item in order.items.all():
            if item.price != 0:
                # Определяем, какой объект используется: product, combo или constructor
                if item.product:
                    product = item.product
                elif item.combo:
                    product = item.combo
                elif item.constructor:
                    product = item.constructor
                
                # Вычисляем и форматируем цену с учётом скидки
                price = Decimal(item.price) * (1 - Decimal(sale_percent) / 100)
                formatted_price = format_price(price)
                
                # Проверяем, что цена больше нуля
                if Decimal(formatted_price) > 0:
                    total_items_sum += Decimal(formatted_price) * item.quantity
                    i = {
                        "description": product.name,
                        "quantity": float(item.quantity),
                        "amount": {
                            "value": formatted_price,
                            "currency": "RUB"
                        },
                        "vat_code": Yookassa.objects.get().vat_code,
                        "payment_mode": "full_prepayment",
                        "payment_subject": "commodity"
                    }
                    
                    items.append(i)
        
        # Добавляем стоимость доставки, если она есть и больше нуля
        if order.delivery_method == 'Доставка' and order.delivery_price > 0:
            formatted_delivery_price = format_price(order.delivery_price)

            if Decimal(formatted_delivery_price) > 0:
                total_items_sum += Decimal(formatted_delivery_price)
                delivery = {
                    "description": 'Доставка',
                    "quantity": 1.000,
                    "amount": {
                        "value": formatted_delivery_price,
                        "currency": "RUB"
                    },
                    "vat_code": Yookassa.objects.get().vat_code,
                    "payment_mode": "full_prepayment",
                    "payment_subject": "service"
                }
                items.append(delivery)
        
        # Используем итоговую сумму заказа для коррекции сумм всех позиций
        total_sum = Decimal(order.summ)
        if total_sum > 0 and total_items_sum != total_sum:
            correction_factor = total_sum / total_items_sum if total_items_sum > 0 else 1
            total_corrected_sum = Decimal(0)

            # Применяем коррекцию ко всем позициям, кроме последней
            for item in items[:-1]:
                item_amount = (Decimal(item['amount']['value']) * correction_factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                item['amount']['value'] = format_price(item_amount)
                total_corrected_sum += item_amount

            # Корректируем последнюю позицию, чтобы итоговая сумма точно совпадала
            last_item = items[-1]
            last_item_amount = (total_sum - total_corrected_sum).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            last_item['amount']['value'] = format_price(last_item_amount)
        else:
            total_sum = format_price(total_items_sum)
        
        # Создаем объект платежа с уникальным ключом идемпотентности
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": format_price(total_sum),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": path + "/orders/confirm/" + str(order.id)
            },
            "capture": True,
            "description": "Заказ №" + str(order.id),
            "metadata": {
                "order_id": str(order.id)
            }, 
            "receipt": {
                "customer": {
                    "full_name": order.name,
                    "phone": str(digits_only)
                },
                "items": items
            }
        }, idempotence_key)

        # Формируем данные для возврата
        data = {
            'id': payment.id,
            'order_id': order.id,
            'confirmation_url': payment.confirmation.confirmation_url,
            'path': path
        }

        
        # Возвращаем данные

        wo_elegram_bot = '5953442472:AAHsgzGdcVrnuJnb0FnDWJ4nrPdDT59YNOE'
        wo_telegram_group = '-1001850576262'

        error_message = str(format_price(total_sum)) + " / " + str(items).replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`')
        send_message(wo_elegram_bot, wo_telegram_group, error_message)
        
        # Возвращаем данные
        return data

    except Exception as e:
        wo_elegram_bot = '5953442472:AAHsgzGdcVrnuJnb0FnDWJ4nrPdDT59YNOE'
        wo_telegram_group = '-1001850576262'

        error_message = str(format_price(total_sum)) + " / " + str(items).replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`') + " / " + str(e)
        send_message(wo_elegram_bot, wo_telegram_group, error_message)
        