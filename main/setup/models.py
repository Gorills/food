from venv import create
from django.db import models
from admin.singleton_model import SingletonModel
from subdomains.models import Subdomain
from main.transliterate_filename import transliterate_file
from sorl.thumbnail import get_thumbnail
# Create your models here.

class BaseSettings(SingletonModel):
    name = models.CharField(max_length=350, blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email_for_order = models.EmailField(blank=True, null=True)

    telegram_bot = models.CharField(blank=True, null=True, max_length=350)
    telegram_group = models.CharField(blank=True, null=True, max_length=350)

    sms_pilot_apikey = models.CharField(blank=True, null=True, max_length=350)
    sms_text = models.CharField(blank=True, null=True, max_length=350)

    copy_year = models.CharField(max_length=350, blank=True, null=True)
    copy = models.CharField(max_length=350, blank=True, null=True)
    city = models.CharField(max_length=350, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)

    vk = models.CharField(max_length=350, blank=True, null=True)
    whatsapp = models.CharField(max_length=350, blank=True, null=True)
    telegram = models.CharField(max_length=350, blank=True, null=True)
    viber = models.CharField(max_length=350, blank=True, null=True)
    ok = models.CharField(max_length=350, blank=True, null=True)
        
    meta_title = models.CharField(max_length=350, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=350, blank=True, null=True)
    meta_h1 = models.CharField(max_length=350, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'setup/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    
    social_image = models.FileField(upload_to=get_image_upload_path, blank=True, null=True)
    logo_light = models.FileField(upload_to=get_image_upload_path, blank=True, null=True)

    logo_height = models.CharField(max_length=250, blank=True, null=True)
    logo_width = models.CharField(max_length=250, blank=True, null=True)
    
    logo_dark = models.FileField(upload_to=get_image_upload_path, blank=True, null=True)
    icon_ico = models.FileField(upload_to=get_image_upload_path, blank=True, null=True)
    icon_png = models.FileField(upload_to=get_image_upload_path, blank=True, null=True)
    icon_svg = models.FileField(upload_to=get_image_upload_path, blank=True, null=True)
    pay_image = models.FileField(upload_to=get_image_upload_path, blank=True, null=True)    
    theme_color = models.CharField(max_length=250, blank=True, null=True)
    time_zone = models.CharField(max_length=250, blank=True, null=True, default='UTC')
    active = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    sms = models.BooleanField(default=False)
    debugging_mode = models.BooleanField(default=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    
    def get_logo(self):
        res = None
        try:
            if self.logo_height and not self.logo_width:
                res = get_thumbnail(self.logo_dark, f'x{self.logo_height}', format="WEBP", crop='center', quality=100)
            elif self.logo_width and not self.logo_height:
                res = get_thumbnail(self.logo_dark, f'{self.logo_width}x', format="WEBP", crop='center', quality=100)
            elif self.logo_height and self.logo_width:
                res = get_thumbnail(self.logo_dark, f'{self.logo_width}x{self.logo_height}', format="WEBP", crop='center', quality=100)
            else:
                res = get_thumbnail(self.logo_dark, 'x60', crop='center', format="WEBP", quality=100)

        except:
            pass

        return res

    # def get_phone(self):
    #     try:
    #         res = self.phone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    #     except:
    #         res = '899999999'
    #     return res
    
    def get_phone(self):

        if self.phone:
            phone_str = self.phone
            phone_list = phone_str.split(',')
            
            
            try:
                res_one = phone_list[0].replace(' ','').replace('-','').replace('(','').replace(')','')
                res_two = phone_list[1].replace(' ','').replace('-','').replace('(','').replace(')','')
                phone = f'<a href="tel:{ res_one }" class="header__contacts-link">{phone_list[0]}</a> <a href="tel:{ res_two }" class="header__contacts-link">{phone_list[1]}</a>'
            except:
                res_one = phone_list[0].replace(' ','').replace('-','').replace('(','').replace(')','')

                phone = f'<a href="tel:{ res_one }" class="header__contacts-link">{phone_list[0]}</a>'
      


        else:
            
            base = BaseSettings.objects.get()
            phone = f'<a href="tel:{ base.get_phone() }" class="header__contacts-link">{base.phone}</a>'

        return phone

   



    




# {{ person.get_engine_display }}
# ENGINE_CHOICES = (
#     ("SQLite", "SQLite"),
#     ("PostgreSQL", "PostgreSQL"),
#     ("MySQL", "MySQL"),
# )

# class DBSettings(models.Model):
#     engine = models.CharField(max_length=250, choices=ENGINE_CHOICES, default='SQLite')
#     name = models.CharField(max_length=250)
#     user = models.CharField(max_length=250)
#     password = models.CharField(max_length=250)
#     host = models.CharField(max_length=250)



class RecaptchaSettings(SingletonModel):
    recaptcha_private_key = models.CharField(max_length=250, blank=True, null=True)
    recaptcha_public_key = models.CharField(max_length=250, blank=True, null=True)
    recaptcha_default_action = models.CharField(max_length=250, default='generic', blank=True, null=True)
    recaptcha_score_threshold = models.CharField(max_length=250, default='0.5', blank=True, null=True)
    recaptcha_language = models.CharField(max_length=250, default='ru', blank=True, null=True)



class EmailSettings(SingletonModel):
    host = models.CharField(max_length=250, blank=True, null=True)
    host_user = models.CharField(max_length=250, blank=True, null=True)
    host_password = models.CharField(max_length=250, blank=True, null=True)
    host_from = models.CharField(max_length=250, blank=True, null=True)
    host_port = models.CharField(max_length=250, default='465', blank=True, null=True)
    use_ssl = models.BooleanField(default=True)
    use_tls = models.BooleanField(default=False)



class CustomCode(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    code = models.TextField(verbose_name='Код')
    h_f = models.BooleanField(verbose_name='Шапка/Подвал')
    subdomain = models.ForeignKey(Subdomain, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Город')


    def __str__(self):
        return self.name
    




class ThemeSettings(SingletonModel):
    THEME_CLASS = (
       ('default', 'Стандартная'),
       ('china', 'Китайский ресторан'),
       ('sushi', 'Суши'),
       
    )
    name = models.CharField(max_length=250, choices=THEME_CLASS, default='sushi')
    


class Colors(SingletonModel):
    primary = models.CharField(max_length=50)
    secondary = models.CharField(max_length=50)
    success = models.CharField(max_length=50, default='#198754')
    danger = models.CharField(max_length=50, default='#dc3545')
    warning = models.CharField(max_length=50, default='#ffc107')
    info = models.CharField(max_length=50, default='#0dcaf0')

    header_bg = models.CharField(max_length=50, default='#ffffff')
    header_font = models.CharField(max_length=50, default='#222222')

    body_bg = models.CharField(max_length=50, default='#ffffff')
    body_font = models.CharField(max_length=50, default='#222222')

    body_bg_light = models.CharField(max_length=50, default='#f7f7fa')
    body_font_light = models.CharField(max_length=50, default='#f7f7fa')


    bg_btn = models.CharField(max_length=50, default='#222222')
    border_btn = models.CharField(max_length=50, default='#222222')
    color_btn = models.CharField(max_length=50, default='#ffffff')
    color_btn_light = models.CharField(max_length=50, default='#222222')






