from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.conf import settings
from accounts.models import UserProfile
from django.contrib.auth.models import User

# Create your models here.
from shop.models import Combo, Product, ProductOption, Ingridients, FoodConstructor



class OrderStatus(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    sort = models.PositiveIntegerField(default=0, verbose_name='Сортировка')
    image = models.ImageField(upload_to='order_status', null=True, blank=True, verbose_name='Изображение')

    ORDER_TYPE_CLASS = (
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
        ('all', 'Все'),
    )

    order_type = models.CharField(max_length=250, choices=ORDER_TYPE_CLASS, default='delivery', verbose_name='Тип заказа')

    def __str__(self):
        return self.name



def default_order_status():
    STATUS_CLASS = (
       ('Новый', 'Новый'),
       ('Готовится', 'Готовится'),
       ('Готов к доставке', 'Готов к доставке'),
       ('Готов к выдаче', 'Готов к выдаче'),
       
       ('Доставлен', 'Доставлен'),
       ('Выполнен', 'Выполнен'),
       ('Отказ', 'Отказ')
    )
    return STATUS_CLASS

def pickup_order_status():
    statuses = OrderStatus.objects.filter(order_type='pickup')
    STATUS_CLASS_SELF_PICKUP = (
        ('Новый', 'Новый'),
        
    )
    if len(statuses) > 0:
        for status in statuses:
            STATUS_CLASS_SELF_PICKUP += ((status.name, status.name),)
    
    else:
        STATUS_CLASS_SELF_PICKUP = (
            ('Новый', 'Новый'),
            ('Готовится', 'Готовится'),
            ('Готов к выдаче', 'Готов к выдаче'),
            ('Выполнен', 'Выполнен'),
            ('Отказ', 'Отказ')
        )

    
    return STATUS_CLASS_SELF_PICKUP



def delivery_order_status():
    statuses = OrderStatus.objects.filter(order_type='delivery')
    STATUS_CLASS_DELIVERY = (
        ('Новый', 'Новый'),
    )
    if len(statuses) > 0:
        for status in statuses:
            STATUS_CLASS_DELIVERY += ((status.name, status.name),)
    
    else:
        STATUS_CLASS_DELIVERY = (
            ('Новый', 'Новый'),
            ('Готовится', 'Готовится'),
            ('Готов к доставке', 'Готов к доставке'),
            ('Доставка', 'Доставка'),
            ('Доставлен', 'Доставлен'),
            ('Выполнен', 'Выполнен'),
            ('Отказ', 'Отказ')
        )

    
    return STATUS_CLASS_DELIVERY
            
    


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
    payment_dop_info = models.CharField(max_length=550, verbose_name="Информация о платеже (ссылка на платеж, токен для Тинькофф)", null=True, blank=True)

    paid = models.BooleanField(default=False)

    summ = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_percent = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Процент скидки")
    bonuses_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    STATUS_CLASS = (
        ('Новый', 'Новый'),
       ('Готовится', 'Готовится'),
       ('Готов к доставке', 'Готов к доставке'),
       ('Готов к выдаче', 'Готов к выдаче'),
       
       ('Доставлен', 'Доставлен'),
       ('Выполнен', 'Выполнен'),
       ('Отказ', 'Отказ')
    )

    STATUS_CLASS_SELF_PICKUP = (
            ('Новый', 'Новый'),
            ('Готовится', 'Готовится'),
            ('Готов к выдаче', 'Готов к выдаче'),
            ('Выполнен', 'Выполнен'),
            ('Отказ', 'Отказ')
        )

    STATUS_CLASS_DELIVERY = (
        ('Новый', 'Новый'),
        ('Готовится', 'Готовится'),
        ('Готов к доставке', 'Готов к доставке'),
        ('Доставка', 'Доставка'),
        ('Доставлен', 'Доставлен'),
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


    def order_views(self):

       
        return self.views.all()
        

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)
    
    def get_status_class_choices(self):
        if self.delivery_method == 'Самовывоз':
            return self.STATUS_CLASS_SELF_PICKUP
        elif self.delivery_method == 'Доставка':
            return self.STATUS_CLASS_DELIVERY
        else:
            # Возвращаем общий список статусов, если метод доставки неизвестен или не выбран
            return self.STATUS_CLASS

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
    



class CustomField(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=250)
    value = models.TextField(max_length=250)




class OrderView(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='views')
    created = models.DateTimeField(auto_now_add=True)