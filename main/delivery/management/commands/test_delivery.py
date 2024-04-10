from django.core.management.base import BaseCommand, CommandError
from orders.models import Order  # Подставьте свой реальный путь до модели Order
from delivery.yandex_eda import yandex_create_order

class Command(BaseCommand):
    help = 'Отображает текущее время'

    def add_arguments(self, parser):
        parser.add_argument('order_id', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        order_ids = kwargs['order_id']
        for order_id in order_ids:
            try:
                order = Order.objects.get(id=order_id)
                yandex_create_order(order)
                # Ваш код обработки заказа
                self.stdout.write(self.style.SUCCESS(f'Заказ с id={order_id} успешно обработан'))
            except Exception as e:

                raise CommandError(e)