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


def format_price(price):
    formatted_price = str(Decimal(price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
    return formatted_price.split('.')[0] + ".00"


    # return f"{price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)}.00"



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

                # Вычисляем и форматируем цену с учётом скидки
                price = Decimal(item.price) * (1 - Decimal(sale_percent) / 100)
                formatted_price = format_price(price)

                if Decimal(formatted_price) > 0:
                    total_items_sum += Decimal(formatted_price) * Decimal(item.quantity)
                    i = {
                        "description": product.name,
                        "quantity": int(item.quantity),  # Количество должно быть целым числом
                        "amount": {
                            "value": formatted_price,
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
                        "value": formatted_delivery_price,
                        "currency": "RUB"
                    },
                    "vat_code": Yookassa.objects.get().vat_code,
                    "payment_mode": "full_prepayment",
                    "payment_subject": "service"
                }
                items.append(delivery)


        total_sum = Decimal(order.summ)

        if total_sum > 0 and total_items_sum != total_sum:
            correction_factor = total_sum / total_items_sum if total_items_sum > 0 else 1
            total_corrected_sum = Decimal(0)

            # Первая корректировка
            for item in items[:-1]:
                corrected_unit_price = (Decimal(item['amount']['value']) * correction_factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                item['amount']['value'] = format_price(corrected_unit_price)

                item_total = corrected_unit_price * Decimal(item['quantity'])
                total_corrected_sum += item_total

            # Последняя позиция после первой корректировки
            last_item = items[-1]
            last_item_total = (total_sum - total_corrected_sum).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            corrected_last_unit_price = (last_item_total / Decimal(last_item['quantity'])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            last_item['amount']['value'] = format_price(corrected_last_unit_price)

            # Проверяем итоговую сумму после первой корректировки
            recalculated_total = sum(Decimal(item['amount']['value']) * Decimal(item['quantity']) for item in items)

            # Вторая корректировка, если суммы не совпадают
            if recalculated_total != total_sum:
                total_corrected_sum = Decimal(0)

                # Перераспределение разницы
                diff = total_sum - recalculated_total
                step_correction = (diff / len(items)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                for item in items[:-1]:
                    corrected_unit_price = (Decimal(item['amount']['value']) + step_correction / Decimal(item['quantity'])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    item['amount']['value'] = format_price(corrected_unit_price)

                    item_total = corrected_unit_price * Decimal(item['quantity'])
                    total_corrected_sum += item_total

                # Корректировка последнего элемента
                last_item = items[-1]
                last_item_total = (total_sum - total_corrected_sum).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                corrected_last_unit_price = (last_item_total / Decimal(last_item['quantity'])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                last_item['amount']['value'] = format_price(corrected_last_unit_price)

            # Проверка окончательной суммы
            final_total = sum(Decimal(item['amount']['value']) * Decimal(item['quantity']) for item in items)
            if final_total != total_sum:
                raise ValueError(f"Ошибка двойной корректировки: итоговая сумма {final_total} не совпадает с {total_sum}")



        error_message = str(format_price(total_sum) + " //// " + str(total_items_sum)) + " //// " + str(items).replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`')
        send_message(wo_elegram_bot, wo_telegram_group, error_message)

        # Создание платежа
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": format_price(total_sum),
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

        # Формируем данные для возврата
        data = {
            'id': payment.id,
            'order_id': order.id,
            'confirmation_url': payment.confirmation.confirmation_url,
            'path': path
        }

        
        # Возвращаем данные

        
        # Возвращаем данные
        return data

    except Exception as e:
        

        error_message = str(format_price(total_sum)) + " / " + str(items).replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`') + " / " + str(e)
        send_message(wo_elegram_bot, wo_telegram_group, error_message)
        