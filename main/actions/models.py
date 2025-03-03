from django.db import models
from shop.models import Product

# Create your models here.





class Action(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    TYPE_CHOICES = (
        ('summ', 'Подарок от суммы'),
        ('plus', 'Товар+Товар'),
        
    )

    action_type = models.CharField(max_length=100, verbose_name='Тип акции', choices=TYPE_CHOICES)

    product = models.ManyToManyField(Product, related_name='actions', verbose_name='Продукты для акции', blank=True)

    summ = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма', blank=True, null=True)

    summ_gift = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма подарка', blank=True, null=True)
    gift_product = models.ForeignKey(Product, related_name='gift_actions', on_delete=models.SET_NULL, verbose_name='Подарок', blank=True, null=True)    

    active_in_pickup = models.BooleanField(default=False, verbose_name='Активна в самовывозе')
    active_in_delivery = models.BooleanField(default=False, verbose_name='Активна в доставке')
    block_balls = models.BooleanField(default=False, verbose_name='Заблокировать баллы')
    block_discount = models.BooleanField(default=False, verbose_name='Заблокировать скидки')

    active = models.BooleanField(default=False, verbose_name='Активна')
    start_date = models.DateField(verbose_name='Начало акции', blank=True, null=True)
    end_date = models.DateField(verbose_name='Окончание акции', blank=True, null=True)


    def __str__(self):
        return self.title