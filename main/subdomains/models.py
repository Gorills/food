from django.db import models

# Create your models here.
class Subdomain(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    subdomain = models.CharField(max_length=255, verbose_name="Субдомен", null=True, blank=True)

    phone = models.CharField(max_length=250, blank=True, null=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True)

    
    telegram_group = models.CharField(blank=True, null=True, max_length=350, verbose_name="Группа телеграм")

    city = models.CharField(max_length=350, blank=True, null=True, verbose_name="Город")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Адрес")

    vk = models.CharField(max_length=350, blank=True, null=True, verbose_name="Вконтакте")
    whatsapp = models.CharField(max_length=350, blank=True, null=True, verbose_name="Whatsapp")
    telegram = models.CharField(max_length=350, blank=True, null=True, verbose_name="Telegram")
    viber = models.CharField(max_length=350, blank=True, null=True, verbose_name="Viber")
    ok = models.CharField(max_length=350, blank=True, null=True, verbose_name="Одноклассники")
        
    meta_title = models.CharField(max_length=350, blank=True, null=True, verbose_name="Meta title")
    meta_description = models.TextField(blank=True, null=True, verbose_name="Meta description")
    meta_keywords = models.CharField(max_length=350, blank=True, null=True, verbose_name="Meta keywords")
    meta_h1 = models.CharField(max_length=350, blank=True, null=True, verbose_name="Meta h1")

    text = models.TextField(blank=True, null=True, verbose_name="Текст")

    zone_file = models.FileField(blank=True, null=True, verbose_name="Файл зоны доставки", upload_to='delivery_zones')
    
    def __str__(self):

        return self.name
    
    def get_phone(self):
        try:
            res = self.phone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        except:
            res = '899999999'
        return res
    

