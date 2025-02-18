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

wo_elegram_bot = '5953442472:AAHsgzGdcVrnuJnb0FnDWJ4nrPdDT59YNOE'
wo_telegram_group = '-1001850576262'


from decimal import Decimal, ROUND_DOWN

def format_price(price):
    """Форматирует цену так, чтобы всегда были две нули после запятой"""
    return f"{price.quantize(Decimal('1'), rounding=ROUND_DOWN)}.00"

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
                if item.product:
                    product = item.product
                elif item.combo:
                    product = item.combo
                elif item.constructor:
                    product = item.constructor
                else:
                    continue

                # Вычисляем цену с учетом скидки и округляем вниз
                price = Decimal(item.price) * (1 - Decimal(sale_percent) / 100)
                formatted_price = format_price(price)

                if Decimal(formatted_price) > 0:
                    total_items_sum += Decimal(formatted_price) * Decimal(item.quantity)
                    i = {
                        "description": product.name,
                        "quantity": int(item.quantity),
                        "amount": {
                            "value": formatted_price,  # Цена всегда с .00
                            "currency": "RUB"
                        },
                        "vat_code": Yookassa.objects.get().vat_code,
                        "payment_mode": "full_prepayment",
                        "payment_subject": "commodity"
                    }
                    items.append(i)

        # Добавляем стоимость доставки, если она есть
        if order.delivery_method == 'Доставка' and order.delivery_price > 0:
            formatted_delivery_price = format_price(order.delivery_price)

            if Decimal(formatted_delivery_price) > 0:
                total_items_sum += Decimal(formatted_delivery_price)
                delivery = {
                    "description": 'Доставка',
                    "quantity": 1,
                    "amount": {
                        "value": formatted_delivery_price,  # Цена всегда с .00
                        "currency": "RUB"
                    },
                    "vat_code": Yookassa.objects.get().vat_code,
                    "payment_mode": "full_prepayment",
                    "payment_subject": "service"
                }
                items.append(delivery)

        total_sum = Decimal(order.summ)

        if total_sum > 0 and total_items_sum != total_sum:
            difference = total_sum - total_items_sum  # Разница между рассчитанной и реальной суммой

            # Корректируем последнюю позицию
            if items:
                last_item = items[-1]
                last_item_total = Decimal(last_item['amount']['value']) * Decimal(last_item['quantity']) + difference
                corrected_last_unit_price = last_item_total / Decimal(last_item['quantity'])
                last_item['amount']['value'] = format_price(corrected_last_unit_price)

            # Проверка окончательной суммы
            final_total = sum(Decimal(item['amount']['value']) * Decimal(item['quantity']) for item in items)
            if final_total != total_sum:
                raise ValueError(f"Ошибка корректировки: итоговая сумма {final_total} не совпадает с {total_sum}")

        # Отправка отладочного сообщения
        error_message = f"{format_price(total_sum)} //// {total_items_sum} //// {items}".replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`')
        send_message(wo_elegram_bot, wo_telegram_group, error_message)

        # Создание платежа
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": format_price(total_sum),  # Цена всегда с .00
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": path + f"/orders/confirm/{order.id}"
            },
            "capture": True,
            "description": f"Заказ №{order.id}",
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

        # Возвращаем данные
        return {
            'id': payment.id,
            'order_id': order.id,
            'confirmation_url': payment.confirmation.confirmation_url,
            'path': path
        }

    except Exception as e:
        error_message = f"{format_price(total_sum)} / {items} / {e}".replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`')
        send_message(wo_elegram_bot, wo_telegram_group, error_message)
