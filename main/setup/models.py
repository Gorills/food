from venv import create
from django.db import models
from admin.singleton_model import SingletonModel
from subdomains.models import Subdomain
from main.transliterate_filename import transliterate_file
from sorl.thumbnail import get_thumbnail
# Create your models here.

class BaseSettings(SingletonModel):
    name = models.CharField(max_length=350, blank=True, null=True)
    ur_name = models.CharField(max_length=350, blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email_for_order = models.EmailField(blank=True, null=True)

    telegram_bot = models.CharField(blank=True, null=True, max_length=350)
    telegram_group = models.CharField(blank=True, null=True, max_length=350)

    sms_pilot_apikey = models.CharField(blank=True, null=True, max_length=350)
    sms_text = models.CharField(blank=True, null=True, max_length=350)

    order_done_title = models.CharField(max_length=350, blank=True, null=True, default="Заказ успешно оформлен!")
    order_done_text = models.TextField(blank=True, null=True, default="Мы свяжемся с Вами в ближайшее время.")

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
    image_compression = models.PositiveIntegerField(blank=True, null=True, default=1)
    
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
                res = get_thumbnail(self.logo_dark, f'x{int(self.logo_height)*self.image_compression}', format="WEBP", crop='center', quality=100)
            elif self.logo_width and not self.logo_height:
                res = get_thumbnail(self.logo_dark, f'{int(self.logo_width)*self.image_compression}x', format="WEBP", crop='center', quality=100)
            elif self.logo_height and self.logo_width:
                res = get_thumbnail(self.logo_dark, f'{int(self.logo_width)*self.image_compression}x{int(self.logo_height)*self.image_compression}', format="WEBP", crop='center', quality=100)
            else:
                res = get_thumbnail(self.logo_dark, 'x60', crop='center', format="WEBP", quality=100)

        except Exception as e:
            print(e)
            pass

        return res

    # def get_phone(self):
    #     try:
    #         res = self.phone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    #     except:
    #         res = '899999999'
    #     return res
    
    def get_phone(self):

        try:

            if self.phone:
                phone_str = self.phone
                phone_list = phone_str.split(',')
                
                
                try:
                    res_one = phone_list[0].replace(' ','').replace('-','').replace('(','').replace(')','')
                    res_two = phone_list[1].replace(' ','').replace('-','').replace('(','').replace(')','')
                    phone = f'''
                    <div class="header__contacts-link-wrap">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M10.2932 8.94914C10.0597 8.81224 9.77266 8.81512 9.54029 8.95316L8.36344 9.65432C8.1 9.81135 7.77099 9.79294 7.52941 9.60428C7.11182 9.27815 6.43942 8.72941 5.85444 8.14444C5.26947 7.55947 4.72074 6.88706 4.3946 6.46947C4.20594 6.22789 4.18753 5.89888 4.34456 5.63544L5.04572 4.4586C5.18434 4.22622 5.18549 3.93689 5.0486 3.70336L3.32187 0.753769C3.15448 0.468473 2.82202 0.328125 2.50049 0.406927C2.18816 0.482853 1.78265 0.668065 1.35758 1.09371C0.026582 2.42471 -0.680332 4.66969 4.325 9.67503C9.33034 14.6804 11.5747 13.974 12.9063 12.6425C13.3325 12.2162 13.5172 11.8102 13.5937 11.4972C13.6713 11.1763 13.5333 10.8461 13.2486 10.6793C12.5376 10.2635 11.0042 9.36558 10.2932 8.94914Z" fill="#D8D8D8"/>
                        </svg>
                        <a href="tel:{ res_one }" class="header__contacts-link header__contacts-phone">{phone_list[0]}</a> 
                        <a href="tel:{ res_two }" class="header__contacts-link header__contacts-phone">{phone_list[1]}</a>
                    </div>'''
                except:
                    res_one = phone_list[0].replace(' ','').replace('-','').replace('(','').replace(')','')

                    phone = f'''
                        
                        <a href="tel:{ res_one }" class="header__contacts-link header__contacts-phone">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M10.2932 8.94914C10.0597 8.81224 9.77266 8.81512 9.54029 8.95316L8.36344 9.65432C8.1 9.81135 7.77099 9.79294 7.52941 9.60428C7.11182 9.27815 6.43942 8.72941 5.85444 8.14444C5.26947 7.55947 4.72074 6.88706 4.3946 6.46947C4.20594 6.22789 4.18753 5.89888 4.34456 5.63544L5.04572 4.4586C5.18434 4.22622 5.18549 3.93689 5.0486 3.70336L3.32187 0.753769C3.15448 0.468473 2.82202 0.328125 2.50049 0.406927C2.18816 0.482853 1.78265 0.668065 1.35758 1.09371C0.026582 2.42471 -0.680332 4.66969 4.325 9.67503C9.33034 14.6804 11.5747 13.974 12.9063 12.6425C13.3325 12.2162 13.5172 11.8102 13.5937 11.4972C13.6713 11.1763 13.5333 10.8461 13.2486 10.6793C12.5376 10.2635 11.0042 9.36558 10.2932 8.94914Z" fill="#D8D8D8"/>
                        </svg>
                        {phone_list[0]}
                        </a>
                    
                    '''
        


            else:

               
                phone = ''

            return phone
        except:
            return ''
    

   



    




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
       ('fast_theme', 'Фаст Тема'),
       ('flowers_light', 'Для цветов светлая'),
       
    )
    name = models.CharField(max_length=250, choices=THEME_CLASS, default='fast_theme')
    


class Colors(SingletonModel):
    primary = models.CharField(max_length=50)
    secondary = models.CharField(max_length=50)
    success = models.CharField(max_length=50, default='#198754')
    danger = models.CharField(max_length=50, default='#dc3545')
    warning = models.CharField(max_length=50, default='#ffc107')
    info = models.CharField(max_length=50, default='#0dcaf0')

    header_bg = models.CharField(max_length=50, default='#ffffff')
    header_font = models.CharField(max_length=50, default='#222222')

    phone_color = models.CharField(max_length=50, default='#222222', verbose_name='Цвет телефона')
    phone_decorations = models.BooleanField(default=False, verbose_name='Подчеркивание телефона')

    footer_color = models.CharField(max_length=50, default='#24262b', verbose_name='Цвет футера')
    footer_font = models.CharField(max_length=50, default='#ffffff', verbose_name='Цвет шрифта футера')

    body_bg = models.CharField(max_length=50, default='#ffffff')
    body_font = models.CharField(max_length=50, default='#222222')

    body_bg_light = models.CharField(max_length=50, default='#f7f7fa')
    body_font_light = models.CharField(max_length=50, default='#f7f7fa')

    cart_border = models.CharField(max_length=50, default='#eaedff', verbose_name='Цвет границы корзины')
    cart_fonts_color = models.CharField(max_length=50, default='#999999', verbose_name='Цвет шрифтов корзины')
    cart_bg = models.CharField(max_length=50, default='#ffffff')

    search_bg = models.CharField(max_length=50, default='#ffffff')
    search_font = models.CharField(max_length=50, default='#222222')
    mobile_menu_bg = models.CharField(max_length=50, default='#ffffff')
    mobile_menu_font = models.CharField(max_length=50, default='#222222')

    gray = models.CharField(max_length=50, default='#f1f2f2')

    product_card_bg = models.CharField(max_length=50, default='#ffffff')
    product_card_font = models.CharField(max_length=50, default='#222222')
    catalog_bg = models.CharField(max_length=50, default='#ffffff')

    bg_btn = models.CharField(max_length=50, default='#222222')
    border_btn = models.CharField(max_length=50, default='#222222')
    color_btn = models.CharField(max_length=50, default='#ffffff')
    color_btn_light = models.CharField(max_length=50, default='#222222')


    bg_image = models.ImageField(upload_to='images_bg', blank=True, null=True)

    header_image = models.ImageField(upload_to='images_bg', blank=True, null=True)
    footer_image = models.ImageField(upload_to='images_bg', blank=True, null=True)
    product_detail_image = models.ImageField(upload_to='images_bg', blank=True, null=True)
    



class Fonts(SingletonModel):

    FONTS_CHOICES = (
        ('Roboto', 'Roboto'),
       
        ('Certa', 'Certa'),
        ('Zombie', 'Zombie'),

    )


    name = models.CharField(max_length=250, choices=FONTS_CHOICES, default='Roboto')
    

    def __str__(self):
        return self.name
