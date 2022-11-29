from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.conf import settings

# Create your models here.
from shop.models import Product, ProductOption

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='user_order')
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='Телефон')
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Адрес')
    address_comment = models.TextField(null=True, blank=True, verbose_name='Комментарий к адресу')

    entrance = models.CharField(max_length=250, null=True, blank=True, verbose_name='Подъезд')
    floor = models.CharField(max_length=250, null=True, blank=True, verbose_name='Этаж')
    flat = models.CharField(max_length=250, null=True, blank=True, verbose_name='Квартира')

    time = models.CharField(max_length=250, null=True, blank=True, verbose_name='Время')
    
    pay_method = models.CharField(max_length=250, verbose_name="Способ оплаты", null=True, blank=True)
    delivery_method = models.CharField(max_length=250, verbose_name="Способ доставка", null=True, blank=True)
    delivery_price = models.CharField(max_length=250, verbose_name="Стоимость доставки", null=True, blank=True)

    order_conmment = models.TextField(null=True, blank=True, verbose_name='Комментарий к заказу')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    summ = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    STATUS_CLASS = (
       ('Новый', 'Новый'),
       ('В работе', 'В работе'),
       ('Обработан', 'Обработан'),
       ('Выполнен', 'Выполнен'),
       ('Отказ', 'Отказ')
    )
    status = models.CharField(max_length=250, verbose_name='Статус заказа', choices=STATUS_CLASS, default='Новый',)
    coupon = models.ForeignKey(Coupon,
                                    related_name='orders',
                                    null=True,
                                    blank=True, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0,
                                        validators=[MinValueValidator(0),
                                                MaxValueValidator(100)])
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

   
    def get_cost(self):
        return self.price * self.quantity