from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.conf import settings
from accounts.models import UserProfile

# Create your models here.
from shop.models import Combo, Product, ProductOption, Ingridients, FoodConstructor

class Order(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='user_order')

    user_pr = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_order')

    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='Телефон')
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Имя')
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Адрес')
    address_comment = models.TextField(null=True, blank=True, verbose_name='Комментарий к адресу')

    entrance = models.CharField(max_length=250, null=True, blank=True, verbose_name='Подъезд')
    floor = models.CharField(max_length=250, null=True, blank=True, verbose_name='Этаж')
    flat = models.CharField(max_length=250, null=True, blank=True, verbose_name='Квартира')
    door_code = models.CharField(max_length=250, null=True, blank=True, verbose_name='Код двери')

    time = models.CharField(max_length=250, null=True, blank=True, verbose_name='Время')
    
    pay_method = models.CharField(max_length=250, verbose_name="Способ оплаты", null=True, blank=True)
    pay_change = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сдача с", null=True, blank=True)
    delivery_method = models.CharField(max_length=250, verbose_name="Способ доставка", null=True, blank=True)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость доставки", null=True, blank=True)

    order_conmment = models.TextField(null=True, blank=True, verbose_name='Комментарий к заказу')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    payment_id = models.CharField(max_length=250, verbose_name="ID платежа", null=True, blank=True)
    payment_dop_info = models.CharField(max_length=550, verbose_name="Информация о платеже (ссылка на плптеж)", null=True, blank=True)

    paid = models.BooleanField(default=False)

    summ = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_percent = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Процент скидки")
    bonuses_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    STATUS_CLASS = (
       ('Новый', 'Новый'),
       ('В работе', 'В работе'),
       ('Обработан', 'Обработан'),
       ('Готов к доставке', 'Готов к доставке'),
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
    
    balls = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percent_pay = models.PositiveIntegerField(null=True, blank=True)

    request_id = models.CharField(max_length=450, verbose_name="ID запроса для доставки", null=True, blank=True)
    delivery_status = models.CharField(max_length=450, verbose_name="Статус доставки", null=True, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))
    

    def get_phone(self):

        digits_only = ''.join(char for char in self.phone if char.isdigit())

        return digits_only




class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, null=True, blank=True)
    options = models.TextField(null=True, blank=True)
    combo = models.ForeignKey(Combo, related_name='order_combo', on_delete=models.CASCADE, null=True, blank=True)
    combo_items = models.TextField(null=True, blank=True)
    constructor = models.ForeignKey(FoodConstructor, related_name='order_constructor', on_delete=models.CASCADE, null=True, blank=True)
    constructor_items = models.TextField(null=True, blank=True)
    free = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.CharField(max_length=250, null=True, blank=True)

   
    def get_cost(self):
        return (self.price * self.quantity) - (self.price * self.free)
    

