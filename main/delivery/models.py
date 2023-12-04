from django.db import models
from admin.singleton_model import SingletonModel

# Create your models here.
class Delivery(SingletonModel):
    
    NAME_CLASS = (
        ('yandex', 'Яндекс.Доставка'),
        
    )
    
    name = models.CharField(max_length=50, verbose_name='Название', choices=NAME_CLASS)
    api_key = models.CharField(max_length=250, verbose_name='Ключ API/token', null=True, blank=True)