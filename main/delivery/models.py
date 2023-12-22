from django.db import models
from admin.singleton_model import SingletonModel

# Create your models here.
class Delivery(SingletonModel):
    
    NAME_CLASS = (
        ('yandex', 'Яндекс.Доставка'),
        
    )
    
    active = models.BooleanField(default=False, verbose_name='Активная')
    name = models.CharField(max_length=50, verbose_name='Название организации или контактного лица', choices=NAME_CLASS)
    api_key = models.CharField(max_length=250, verbose_name='Ключ API/token', null=True, blank=True)

    min_summ = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Минимальная сумма', null=True, blank=True)
    free_summ = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма бесплатной доставки', null=True, blank=True)

    city = models.CharField(max_length=250, verbose_name='Город', null=True, blank=True)
    address = models.CharField(max_length=250, verbose_name='Адрес', null=True, blank=True)
    adress_dot = models.CharField(max_length=250, verbose_name='Адрес в формате координат', null=True, blank=True)
    floor = models.CharField(max_length=250, verbose_name='Этаж', null=True, blank=True)
    flat = models.CharField(max_length=250, verbose_name='Квартира', null=True, blank=True)
    comment = models.CharField(max_length=250, verbose_name='Комментарий для курьера', null=True, blank=True)
    email = models.CharField(max_length=250, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=250, verbose_name='Телефон', null=True, blank=True)


    sale_persent = models.PositiveIntegerField(verbose_name='Процент скидки на доставку (компенсация за доставку)', null=True, blank=True)
    summ_persent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма заказа, от которой начинает работать компенсация за доставку', null=True, blank=True)
    delivery_summ_persent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма доставки, от которой начинает работать компенсация за доставку', null=True, blank=True)

    def __str__(self):
        return self.name