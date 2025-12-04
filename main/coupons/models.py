
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код купона')
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True, verbose_name='Slug')
    valid_from = models.DateField(verbose_name='Действителен с')
    valid_to = models.DateField(verbose_name='Действителен до')
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Скидка (%)'
    )
    active = models.BooleanField(default=True, verbose_name='Активен')

    TYPE_CHOICES = (
        ('all', 'Все'),
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
    )

    promo_type = models.CharField(
        max_length=20, 
        default='all', 
        choices=TYPE_CHOICES, 
        verbose_name="Действие купона"
    )
    
    # Дополнительные поля для аналитики
    max_uses = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name='Максимальное количество использований',
        help_text='Оставьте пустым для неограниченного использования'
    )
    
    current_uses = models.PositiveIntegerField(
        default=0,
        verbose_name='Текущее количество использований'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return self.code
    
    def is_valid(self):
        """Проверяет, действителен ли купон"""
        now = timezone.now().date()
        
        # Проверка активности
        if not self.active:
            return False
        
        # Проверка дат
        if now < self.valid_from or now > self.valid_to:
            return False
        
        # Проверка лимита использований
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        
        return True
    
    def increment_usage(self):
        """Увеличивает счетчик использований"""
        self.current_uses += 1
        self.save(update_fields=['current_uses'])

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
        ordering = ['-created_at']


class CouponUsageLog(models.Model):
    """
    Модель для логирования использования промокодов
    """
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name='usage_logs',
        verbose_name='Купон'
    )
    
    user_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Телефон пользователя'
    )
    
    user_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP адрес'
    )
    
    order_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='ID заказа'
    )
    
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма скидки'
    )
    
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Сумма заказа'
    )
    
    success = models.BooleanField(
        default=True,
        verbose_name='Успешно применен'
    )
    
    error_message = models.TextField(
        null=True,
        blank=True,
        verbose_name='Сообщение об ошибке'
    )
    
    used_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата использования'
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name='User Agent'
    )
    
    def __str__(self):
        return f'{self.coupon.code} - {self.used_at.strftime("%Y-%m-%d %H:%M")}'
    
    class Meta:
        verbose_name = 'Лог использования купона'
        verbose_name_plural = 'Логи использования купонов'
        ordering = ['-used_at']
        indexes = [
            models.Index(fields=['coupon', '-used_at']),
            models.Index(fields=['user_phone', '-used_at']),
        ]