from django.db import models
from admin.singleton_model import SingletonModel
# Create your models here.


class Integrations(SingletonModel):

    NAME_CLASS = (
        ('iiko', 'iiko'),
    )
    name = models.CharField(max_length=50, choices=NAME_CLASS, verbose_name='Название')

    api_key = models.CharField(max_length=50, verbose_name='Ключ API')
    webhook_uri = models.CharField(max_length=50, null=True, blank=True, verbose_name='Хендлер (не обязательно)')
    webhook_token = models.CharField(max_length=64, null=True, blank=True, verbose_name='Токен (не обязательно)')
    

class CronTab(models.Model):
    minutes = models.CharField(max_length=50, verbose_name='Минуты')
    hours = models.CharField(max_length=50, verbose_name='Часы')
    integration = models.ForeignKey(Integrations, on_delete=models.CASCADE, related_name='cron_tab', verbose_name='Интеграция')
    row_number = models.CharField(max_length=250, verbose_name='Номер задания')

