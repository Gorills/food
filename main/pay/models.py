from django.db import models
from admin.singleton_model import SingletonModel
# Create your models here.
class PaymentSet(SingletonModel):
    PAY_CLASS = (
       ('yookassa', 'ЮКасса'),
       ('paykeeper', 'PayKeeper'),
    #    ('alfabank', 'AlfaBank'),
    )
    name = models.CharField(max_length=250, choices=PAY_CLASS, verbose_name='Платежная система')
    status = models.BooleanField(default=False, verbose_name='Включить онлайн оплаты')




class Yookassa(SingletonModel):
    shop_id = models.CharField(max_length=250, verbose_name='ID магазина')
    key = models.CharField(max_length=250, verbose_name='Секретный ключ')
    test = models.BooleanField(default=False, verbose_name='Тестовые платежи')
    VAT_CODES = (
       ('1', 'Без НДС'),
       ('2', 'НДС по ставке 0%'),
       ('3', 'НДС по ставке 10%'),
       ('4', 'НДС чека по ставке 20%'),
       ('5', 'НДС чека по расчетной ставке 10/110'),
       ('6', 'НДС чека по расчетной ставке 20/120'),

    )
    vat_code = models.CharField(max_length=250, verbose_name='Код ставки НДС ', choices=VAT_CODES)


class AlfaBank(SingletonModel):
    login = models.CharField(max_length=250, verbose_name='Логин API')
    password = models.CharField(max_length=250, verbose_name='Пароль API')

    token = models.CharField(max_length=250, verbose_name='Token', null=True, blank=True)



class PayKeeper(SingletonModel):
    login = models.CharField(max_length=250, verbose_name='Логин')
    password = models.CharField(max_length=250, verbose_name='Пароль')
    server = models.CharField(max_length=250, verbose_name='Сервер (вместе с протоколом https://)', default='https://demo.paykeeper.ru')

    