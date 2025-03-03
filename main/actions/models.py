from django.utils import timezone

from django.db import models
from shop.models import Category, Product

# Create your models here.





class Action(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )
    
    working_days = models.JSONField(
        default=list,
        verbose_name='Дни работы акции',
        blank=True,
        help_text='Выберите дни недели, когда акция активна'
    )


    title = models.CharField(max_length=100, verbose_name='Название')
    TYPE_CHOICES = (
        ('summ', 'Подарок от суммы'),
        ('plus', 'Товар+Товар'),
        ('cats', 'Товары категории'),
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', blank=True, null=True)
    pruduct_numbers = models.PositiveIntegerField(verbose_name='Количество товаров', blank=True, null=True)

    action_type = models.CharField(max_length=100, verbose_name='Тип акции', choices=TYPE_CHOICES)

    product = models.ManyToManyField(Product, related_name='actions', verbose_name='Продукты для акции', blank=True)

    summ = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма', blank=True, null=True)

    
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
    

    def is_active_today(self):
        """Проверка, активна ли акция сегодня"""
        if not self.active:
            return False
        
        # Если дни не указаны или список пустой, акция активна всегда
        if not self.working_days:
            return True
            
        today = timezone.now().weekday()
        return today in self.working_days