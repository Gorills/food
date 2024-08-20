
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    TYPE_CHOICES = (
        ('all', 'Все'),
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
        
    )

    promo_type = models.CharField(max_length=20, default='all', choices=TYPE_CHOICES, verbose_name="Действие купона")

    def __str__(self):
        return self.code

    class Meta:
      
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'