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


class UserRigts(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rights')
    view_all_statictic = models.BooleanField(default=False, verbose_name='Просмотр статистики')
    add_workers = models.BooleanField(default=False, verbose_name='Добавлять/удалять сотрудников')
    add_statics = models.BooleanField(default=False, verbose_name='Добавлять/удалять статичные страницы')
    add_sliders = models.BooleanField(default=False, verbose_name='Добавлять/удалять слайдеры')
    change_shop_settings = models.BooleanField(default=False, verbose_name='Изменять настройки магазина')
    change_delivery_periods = models.BooleanField(default=False, verbose_name='Изменять периоды доставки')
    change_time_sales = models.BooleanField(default=False, verbose_name='Изменять время скидок на товары')
    add_categorys = models.BooleanField(default=False, verbose_name='Добавлять/удалять категории')
    add_products = models.BooleanField(default=False, verbose_name='Добавлять/удалять товары')
    add_relateds = models.BooleanField(default=False, verbose_name='Добавлять/удалять сопутствующие товары')
    add_combos = models.BooleanField(default=False, verbose_name='Добавлять/удалять комбо')
    add_constructors = models.BooleanField(default=False, verbose_name='Добавлять/удалять конструкторы')
    add_options = models.BooleanField(default=False, verbose_name='Добавлять/удалять опции')
    add_chars = models.BooleanField(default=False, verbose_name='Добавлять/удалять характеристики')
    upload_csv = models.BooleanField(default=False, verbose_name='Загружать данные из CSV')
    view_customers = models.BooleanField(default=False, verbose_name='Просмотреть клиентов')
    view_orders = models.BooleanField(default=False, verbose_name='Просмотреть заказы')
    add_posts = models.BooleanField(default=False, verbose_name='Добавлять/удалять посты')
    add_propmo = models.BooleanField(default=False, verbose_name='Добавлять/удалять промокоды')
    redact_loyal_cart = models.BooleanField(default=False, verbose_name='Редактировать карты лояльности')
    add_reviews = models.BooleanField(default=False, verbose_name='Добавлять/удалять отзывы')
    change_settings = models.BooleanField(default=False, verbose_name='Изменять общие настройки сайта')
    add_pay_systems = models.BooleanField(default=False, verbose_name='Добавлять/удалять платежные системы')
    add_delivery_service = models.BooleanField(default=False, verbose_name='Добавлять/удалять службы доставки')
    add_codes = models.BooleanField(default=False, verbose_name='Добавлять/удалять коды счетчиков')
    add_subdomains = models.BooleanField(default=False, verbose_name='Добавлять/удалять субдомены')
    add_integrations = models.BooleanField(default=False, verbose_name='Добавлять/удалять интеграции')
    change_design = models.BooleanField(default=False, verbose_name='Изменять дизайн')


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
            try:
                result = max([x for x in SUMM_LIST if x <= summ])
            except:
                result = 0
            # Дополнительный код, использующий переменную result
        else:
            result=0

        card_status = LoyaltyCardStatus.objects.get(summ=result)
        return card_status
    


class LoyaltyCardHistory(models.Model):

    order_id = models.CharField(max_length=50, verbose_name='Номер заказа', null=True, blank=True)
    card = models.ForeignKey(LoyaltyCard, on_delete=models.CASCADE, related_name='history')
    summ = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма покупок')
    balls = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество баллов')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    TYPE_COICE = (
        ('add', 'Добавление баллов'),
        ('pay', 'Оплата баллами'),
    )

    operation_type = models.CharField(max_length=50, verbose_name='Тип операции', choices=TYPE_COICE, default='add')

    def __str__(self):
        return f'{self.card.user.phone} - {self.summ} - {self.balls} - {self.date} - {self.operation_type}'