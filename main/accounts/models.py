from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from admin.singleton_model import SingletonModel
# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True, null=True, unique=True)
    use_sms = models.BooleanField(default=True)
    
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.phone


    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False



class LoyaltyCardSettings(SingletonModel):
    active = models.BooleanField(default=False, verbose_name='Включить карты лояльности')
    status_down = models.BooleanField(default=True, verbose_name='Скидка')
    status_up = models.BooleanField(default=False, verbose_name='Накопление')
    show_status = models.BooleanField(default=True, verbose_name='Отображать статус карты в кабинете пользователя')
    show_summ = models.BooleanField(default=True, verbose_name='Отображать сумму покупок в кабинете пользователя')
    

    balls_min_summ = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Минимальная сумма покупки для оплаты баллами (нельзя оплатить баллами сумму ниже)')
    exclude_combos = models.BooleanField(default=False, verbose_name='Исключить Комбо наборы')
    exclude_sales = models.BooleanField(default=False, verbose_name='Исключить акционные товары')
    remove_sale_price = models.BooleanField(default=False, verbose_name='Отменить скидку у акционных товаров при применении бонусов')

    enable_add_balls_after_first_order = models.BooleanField(default=False, verbose_name='Разрешить добавлять баллы только после первого заказа')
    balls_after_first_order = models.PositiveIntegerField(default=0, verbose_name='Колличество баллов после первого заказа')
    first_order_summ_for_add_balls = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма первого заказа для начисления баллов')

    send_sms = models.BooleanField(default=True, verbose_name='Отправлять СМС при начислении баллов')
    sms_text = models.TextField(verbose_name='СМС текст при начислении баллов', blank=True, null=True, default='Вам начислено {balls} баллов - {sitename}')

    text = models.TextField(verbose_name='Описание программы лояльности')


class LoyaltyCardStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название статуса карты')
    summ = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма для получения')
    percent_up = models.PositiveIntegerField(default=0, verbose_name='Процент зачисления при накоплении')
    percent_down = models.PositiveIntegerField(default=0, verbose_name='Процент скидки при оплате')
    percent_down_pickup = models.PositiveIntegerField(default=0, verbose_name='Процент скидки при самовывозе')

    percent_pay = models.PositiveIntegerField(default=0, verbose_name='Процент оплаты накопленными баллами')
    percent_pay_pickup = models.PositiveIntegerField(default=0, verbose_name='Процент оплаты баллами при самовывозе')



class LoyaltyCard(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='card')
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    summ = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма покупок')
    balls = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Количество баллов')
    

    def status(self):

        card_statuses = LoyaltyCardStatus.objects.all()

        summ = self.summ

        SUMM_LIST = []


        for status in card_statuses:
            SUMM_LIST.append(status.summ)

        
        if SUMM_LIST:
            result = max([x for x in SUMM_LIST if x <= summ])
            # Дополнительный код, использующий переменную result
        else:
            result=0

        card_status = LoyaltyCardStatus.objects.get(summ=result)
        return card_status