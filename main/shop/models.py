import math
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from admin.singleton_model import SingletonModel
from subdomains.models import Subdomain
from sorl.thumbnail import get_thumbnail
from main.transliterate_filename import transliterate_file

# Create your models here.


class ShopSetup(SingletonModel):
    STATUS_CLASS = (
       ('hide', 'Скрыть'),
       ('out_of_stock', 'Статус: нет в налчии'),
       ('to_order', 'Статус: под заказ'),
    )
    work_time = models.CharField(max_length=250, verbose_name='Время работы', null=True, blank=True)

    start_delivery = models.TimeField(default="10:00:00", verbose_name='Время начала доставки (указывайте время с интервалом в 30 минут, значения с другими параметрами может вызвать ошибку)')
    end_delivery = models.TimeField(default="21:00:00", verbose_name='Время окончания доставки (указывайте время с интервалом в 30 минут, значения с другими параметрами может вызвать ошибку)')

    delivery_full = models.BooleanField(default=False, verbose_name='Доставка 24/7')
    delay = models.PositiveIntegerField(default=1, verbose_name='Задержка при формировании заказа на доставку. Считается так: текущее время + время задержки')
    interval = models.PositiveIntegerField(default=30, verbose_name='Интервалы по времени доставки в минутах')

    only_pay_with_delivery = models.BooleanField(default=False, verbose_name='Доставка только при оплате онлайн')
    info_to_order_anyway = models.BooleanField(default=False, verbose_name='Отправлять информацию о заказе в телеграм, даже если оплата не прошла')
    zones_delivery = models.BooleanField(default=False, verbose_name='Включить зоны доставки')

    price_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость доставки', default=0)
    free_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма заказа для бесплатной доставки', default=0)
    min_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Минимальная сумма заказа для доставки', default=0)

    show_descrioption = models.BooleanField(default=False, verbose_name='Показать короткое описание товара под карточкой')
    
    status = models.CharField(max_length=250, verbose_name='Товар при 0 остатке', choices=STATUS_CLASS, default='out_of_stock')
    description = models.TextField(null=True, blank=True, verbose_name='Описание каталога')
    meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name='h1')
    meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name='Мета тайтл')
    meta_description = models.TextField(null=True, blank=True, verbose_name='Мета описание')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='Ключевые слова через запятую')
    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'shopsetup/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    
    image = models.ImageField(upload_to=get_image_upload_path, null=True, blank=True, verbose_name='Изображение')
    action = models.BooleanField(default=True, verbose_name='Включить акции')
    new_products = models.BooleanField(default=True, verbose_name='Включить новинки')
    sales_hits = models.BooleanField(default=True, verbose_name='Включить хиты продаж')
    first_delivery = models.PositiveIntegerField(default=0, verbose_name='Скидка на первый заказ')
    discount_on_pickup = models.PositiveIntegerField(default=0, verbose_name='Скидка при самовывозе')

    all_menus = models.BooleanField(default=False, verbose_name='Показывать весь ассортимент на главной странице')

    start_bonus = models.PositiveIntegerField(default=0, verbose_name='Количество бонусов при регистрации')

    min_width = models.PositiveIntegerField(null=True, blank=True, default=290, verbose_name='Ширина миниатюры')
    min_height = models.PositiveIntegerField(null=True, blank=True, default=193, verbose_name='Высота миниатюры')
    max_width = models.PositiveIntegerField(null=True, blank=True, default=750, verbose_name='Ширина основного изображения')
    max_height = models.PositiveIntegerField(null=True, blank=True, default=500, verbose_name='Высота основного изображения')


    delivery_blocked = models.BooleanField(default=False, verbose_name='Заблокировать доставку')
    delivery_blocked_text = models.TextField(null=True, blank=True, verbose_name='Текст блокировки доставки')




class DeliveryTimePrice(models.Model):
    start_delivery = models.TimeField(default="10:00:00", verbose_name='Время начала периода')
    end_delivery = models.TimeField(default="21:00:00", verbose_name='Время окончания периода')
    price_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость доставки', default=0)
    
    free_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма заказа для бесплатной доставки', default=0)
    min_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Минимальная сумма заказа для доставки', default=0)

    class Meta:
        verbose_name = 'Период доставки'
        verbose_name_plural = 'Периоды доставки'



class WorkDay(models.Model):

    DAY_CLASS = (
       (0, 'Понедельник'),
       (1, 'Вторник'),
       (2, 'Среда'),
       (3, 'Четверг'),
       (4, 'Пятница'),
       (5, 'Суббота'),
       (6, 'Воскресенье'),
    )

    day = models.PositiveIntegerField(verbose_name='День недели', choices=DAY_CLASS, unique=True)
    start_delivery = models.TimeField(default="10:00", verbose_name='Время начала доставки', null=True, blank=True)
    end_delivery = models.TimeField(default="21:00", verbose_name='Время окончания доставки', null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name='Рабочий день недели')

  
    class Meta:
        verbose_name = 'Рабочий день недели'
        verbose_name_plural = 'Рабочие дни недели'


class PickupAreas(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название филиала (для внутреннего использования)')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    time_to_open = models.CharField(max_length=250, verbose_name='Время открытия (не обязательно)', null=True, blank=True)
    time_to_close = models.CharField(max_length=250, verbose_name='Время закрытия (не обязательно)', null=True, blank=True)
    all_time = models.BooleanField(default=False, verbose_name='Работает 24/7')
    dop_info = models.CharField(max_length=250, null=True, blank=True, verbose_name='Дополнительные условия работы (выходные)')
    show_to_contacts = models.BooleanField(default=False, verbose_name='Показывать в контактах (не обязательно)')
    phone = models.CharField(max_length=18, null=True, blank=True, verbose_name='Телефон (не обязательно)')
    city = models.ForeignKey(Subdomain, on_delete=models.CASCADE, verbose_name='Город', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_phone(self):

        try:
            res = self.phone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        except:
            res = '899999999'

        return res


class PayMethod(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название способа оплаты')
    in_pay_delivery = models.BooleanField(default=False, verbose_name='Включить в способ оплаты доставки')
    in_pay_pickup = models.BooleanField(default=True, verbose_name='Включить в способ оплаты самовывоза')

    def __str__(self):
        return self.name


class Category(models.Model):
    external_id = models.CharField(max_length=250, null=True, blank=True, unique=True)
    name = models.CharField(max_length=350)
    description = models.TextField(null=True, blank=True)
    meta_h1 = models.CharField(max_length=350, null=True, blank=True)
    meta_title = models.CharField(max_length=350, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)

    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'categories/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    
    image = models.ImageField(upload_to=get_image_upload_path, null=True, blank=True)
    top = models.BooleanField()
    home = models.BooleanField(default=False, verbose_name='Отображать на главной странице')
    resize = models.BooleanField(default=False, verbose_name='Растянуть фон')
    font_color = models.CharField(max_length=250, null=True, blank=True, verbose_name='Цвет шрифта')
    bg_color = models.CharField(max_length=250, default='#ffffff', null=True, blank=True, verbose_name='Цвет фона')
    opacity = models.PositiveIntegerField(default=100, verbose_name='Прозрачность изображения')

    column = models.PositiveIntegerField(default=1)
    sort_order = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, max_length=250)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.name
    

    def all_active_products(self):

        products = self.products.filter(status=True, stock__gt=0)
        childrens = Category.objects.filter(parent=self)
        children_products = Product.objects.filter(parent__in=childrens)
        products = products | children_products


        return products

    # def get_parent_path(self, list=None):
    #     parenturl = []
    #     if list is not None:
    #         parenturl = list
    #     if self.parent is not None:
    #         parenturl.insert(0,self.parent.slug)
    #         return self.parent.get_parent_path(parenturl)
    #     return parenturl
    # def get_absolute_url(self):
    #     path = ''
    #     if self.parent is not None:
    #         parentlisting = self.get_parent_path()
    #         for parent in parentlisting:
    #             path = path + parent + '/'
    #     return reverse("category_detail", kwargs={"path": path, "slug": self.slug})


    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    

    class Meta:
      
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    


class Manufacturer(models.Model):
    name = models.CharField(max_length=350)
    description = models.TextField(null=True, blank=True, default=' ')
    meta_h1 = models.CharField(max_length=350, null=True, blank=True)
    meta_title = models.CharField(max_length=350, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)

    slug = models.SlugField(unique=True, max_length=250)
    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'manufacturer/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    image = models.ImageField(upload_to=get_image_upload_path, null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0, null=True, blank=True)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)




    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

from itertools import groupby
from django.db.models import Q


import datetime

import time

def check_time(product_sale):
    now_day = datetime.datetime.now().strftime('%Y-%m-%d')
    day = datetime.datetime.strptime(now_day, '%Y-%m-%d')
    now_get = datetime.datetime.now().strftime('%H:%M:%S')
    now = datetime.datetime.strptime(now_get, '%H:%M:%S')

    try: 
        date_start = datetime.datetime.strptime(str(product_sale.date_start), '%Y-%m-%d')
    except:
        date_start = None
    
    try:
        date_end = datetime.datetime.strptime(str(product_sale.date_end), '%Y-%m-%d')
    except:
        date_end = None

    if date_start and date_end:
        if date_start <= day <= date_end:
            try:
                start = datetime.datetime.strptime(str(product_sale.time_start), '%H:%M:%S')
            except:
                start = None
            try:
                end = datetime.datetime.strptime(str(product_sale.time_end), '%H:%M:%S')
            except:
                end = None

            if start and end:
                if start <= now <= end:
                    return True
                else:
                    return False
            elif start and not end:
                if start <= now:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    elif date_start and not date_end:
        if date_start <= day:
            try:
                start = datetime.datetime.strptime(str(product_sale.time_start), '%H:%M:%S')
            except:
                start = None
            try:
                end = datetime.datetime.strptime(str(product_sale.time_end), '%H:%M:%S')
            except:
                end = None

            if start and end:
                if start <= now <= end:
                    return True
                else:
                    return False
            elif start and not end:
                if start <= now:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    elif not date_start and date_end:
        if date_end >= day:
            try:
                start = datetime.datetime.strptime(str(product_sale.time_start), '%H:%M:%S')
            except:
                start = None
            try:
                end = datetime.datetime.strptime(str(product_sale.time_end), '%H:%M:%S')
            except:
                end = None

            if start and end:
                if start <= now <= end:
                    return True
                else:
                    return False
            elif start and not end:
                if start <= now:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    else:
        try:
            start = datetime.datetime.strptime(str(product_sale.time_start), '%H:%M:%S')
        except:
            start = None
        try:
            end = datetime.datetime.strptime(str(product_sale.time_end), '%H:%M:%S')
        except:
            end = None

        if start and end:
            if start <= now <= end:
                return True
            else:
                return False
        elif start and not end:
            if start <= now:
                return True
            else:
                return False
        else:
            return False


class Product(models.Model):
    external_id = models.CharField(max_length=250, null=True, blank=True, unique=True)
    # Выводить в меню и других списках
    name = models.CharField(max_length=350, verbose_name='Название')
    # Короткое описание, которое выводится в каталоге товаров, если есть
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # Если нет, то выводим name
    meta_h1 = models.CharField(max_length=350, null=True, blank=True)
    # Если нет, то выводим name
    meta_title = models.CharField(max_length=350, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    # Тэги через запятую (сделать сортировку по ним)
    tags = models.TextField(null=True, blank=True)
    
    # Артикул
    sku = models.CharField(max_length=350, null=True, blank=True)
    
    # Цена с учетом скидки
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    # Цена до скидки
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Количество
    stock = models.PositiveIntegerField(default=1)
    # Количество продаж
    sales = models.PositiveIntegerField(default=0)
    # Минимум для заказа
    minimum = models.PositiveIntegerField(null=True, blank=True, default=1)

    # Вычитать со склада
    subtract = models.BooleanField(default=False)
    # Необходима доставка
    shipping = models.BooleanField(default=True)
    # Новинка
    new = models.BooleanField(default=False)
    # Бестселлер
    bestseller = models.BooleanField(default=False)

    slug = models.SlugField(unique=True, max_length=250, null=True)

    # Дата поступления
    date_available = models.DateField(auto_now_add=True)

    # Настройка параметров товара
    length = models.CharField(max_length=200, null=True, blank=True)
    width = models.CharField(max_length=200, null=True, blank=True)
    height = models.CharField(max_length=200, null=True, blank=True)
    

    LENGHT_CLASS = (
       ('см', 'Сантиметры'),
       ('мм', 'Миллиметры'),
    )
    length_class = models.CharField(max_length=200, choices=LENGHT_CLASS, default='см', null=True, blank=True)
    weight = models.CharField(max_length=200, null=True, blank=True)
    WEIGHT_CLASS = (
       ('кг', 'Киллограмы'),
       ('гр', 'Граммы'),
    )
    weight_class = models.CharField(max_length=200, choices=WEIGHT_CLASS, default='гр', null=True, blank=True)

    # Связи
    product_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='manufacturer_products', null=True, blank=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True, verbose_name='Категория')

    # Связанные товары
    product_connect = models.ManyToManyField('self', related_name='connects', blank=True)

    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'products/thumb/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    
    # Маленькое изображение
    thumb = models.FileField(upload_to=get_image_upload_path, verbose_name='Основное изображение', null=True, blank=True)
    
    

    # Показывать/не показывать. Возможность скрыть товар
    status = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)    


    # Если товар сопутствующий
    related = models.BooleanField(default=False, verbose_name='Сделать сопутствующим')
    all_cats = models.BooleanField(default=True, verbose_name='Отображать во всех категориях')
    free = models.PositiveIntegerField(default=0, verbose_name='Бесплатно в заказе')
    minimum = models.PositiveIntegerField(default=1, verbose_name='Минимальное количество')
    
    # iiko
    iiko_type = models.CharField(max_length=200, null=True, blank=True, default='Dish')



    def get_thumb_mini(self):
        res = None
        setup = ShopSetup.objects.get()
        try:
            if setup.min_height and not setup.min_width:
                res = get_thumbnail(self.thumb, f'x{setup.min_height}', format="WEBP", crop='center', quality=100)
            elif setup.min_width and not setup.min_height:
                res = get_thumbnail(self.thumb, f'{setup.min_width}x', format="WEBP", crop='center', quality=100)
            elif setup.min_height and setup.min_width:
                res = get_thumbnail(self.thumb, f'{setup.min_width}x{setup.min_height}', format="WEBP", crop='center', quality=100)
            else:
                res = get_thumbnail(self.thumb, '290x193', crop='center', format="WEBP", quality=100)

            res = res.url
        except Exception as e:
            res = '/core/libs/no-image.webp'
             

        return res
    
    def get_thumb_maxi(self):
        res = None
        setup = ShopSetup.objects.get()
        try:
            if setup.max_height and not setup.max_width:
                res = get_thumbnail(self.thumb, f'x{setup.max_height}', format="WEBP", crop='center', quality=100)
            elif setup.max_width and not setup.max_height:
                res = get_thumbnail(self.thumb, f'{setup.max_width}x', format="WEBP", crop='center', quality=100)
            elif setup.max_height and setup.max_width:
                res = get_thumbnail(self.thumb, f'{setup.max_width}x{setup.max_height}', format="WEBP", crop='center', quality=100)
            else:
                res = get_thumbnail(self.thumb, '750x500', crop='center', format="WEBP", quality=100)

            res = res.url
        except:
            res = '/core/libs/no-image.webp'

        
        return res

    def __str__(self):
        
        return self.name

    def get_absolute_url(self):

        try:
            return reverse("product_detail", kwargs={"parent": self.parent.slug, "slug": self.slug})
        except:
            return('')
    
    def get_sale(self):

        product_sale = ProductSale.objects.filter(Q(categorys=self.parent) | Q(products=self)).prefetch_related('categorys', 'products').first()

        
        if not product_sale:
            try:
                old = self.old_price
                new = self.price
                razn = old - new
                persent = (razn/old)*100
                return persent
            except:
                return None
        
        else:

            get_time = check_time(product_sale)
            
            if get_time:
                return product_sale.percent
            else:
                try:
                    old = self.old_price
                    new = self.price
                    razn = old - new
                    persent = (razn/old)*100
                    return persent
                except:
                    return None
        

    
    def get_price_after_sale(self):

        get_sale = self.get_sale()
        
        product_sale = ProductSale.objects.filter(Q(categorys=self.parent) | Q(products=self)).prefetch_related('categorys', 'products').first()

        if not product_sale or not get_sale:
            return self.price

        percent = product_sale.percent
        rounding_up = product_sale.rounding_up

        if rounding_up:
            return math.ceil(self.price - (self.price * percent / 100))
        else:
            return self.price - (self.price * percent / 100)

        

    def get_old_price(self):
        get_sale = self.get_sale()
        product_sale = ProductSale.objects.filter(Q(categorys=self.parent) | Q(products=self)).prefetch_related('categorys', 'products').first()

        
        if not product_sale or not get_sale: 
            return self.old_price
        else:

            return self.price
     

        
    def get_first_select(self):
        try:
            select_parent = None
            
            for option in self.options.all():
                if option.type.option_class == 'select':
                    select_parent = option.type
                    break
            
            if not select_parent:
                return None
            
            select_option = select_parent.t_options.filter(type__option_class='select', parent=self)
            
            if not select_option:
                return None
            
            return select_option
        except:
            return None

    def get_all_options(self):

        try:

            first_select = self.get_first_select()

            if first_select is not None:
                
                # Получить список идентификаторов опций, находящихся в `first_select`
                first_select_ids = first_select.values_list('id', flat=True)

                # Исключить опции с указанными идентификаторами
                select_option = self.options.exclude(id__in=first_select_ids)


                products_op = []
                for pr in select_option:
                    products_op.append(pr.id)

            

                types = OptionType.objects.filter(t_options__in=select_option)

                options_type = []
                for t in types:
                    options_type.append(t.id)
                
                new_x = [el for el, _ in groupby(options_type)]

                filter_types = OptionType.objects.filter(id__in=new_x).exclude(option_class='select')


                return filter_types
            


            else:
                select_option = self.options.all()
                
                products_op = []
                for pr in select_option:
                    products_op.append(pr.id)

            

                types = OptionType.objects.filter(t_options__in=select_option)

                options_type = []
                for t in types:
                    options_type.append(t.id)
                
                new_x = [el for el, _ in groupby(options_type)]

                filter_types = OptionType.objects.filter(id__in=new_x).exclude(option_class='select')


                return filter_types
        except:
            return None
        
            


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'products/images/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    src = models.ImageField(upload_to=get_image_upload_path)
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'



class OptionType(models.Model):
    OPTION_CLASS = (
     
    #    ('radio', 'Переключатель'),
       ('checkbox', 'Флажки'),
       ('select', 'Выпадающий список'),
      
    )
    name = models.CharField(max_length=250)
    option_class = models.CharField(max_length=200, choices=OPTION_CLASS, default='select')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип опции'
        verbose_name_plural = 'Типы опций'


class ProductOption(models.Model):
    
    type = models.ForeignKey(OptionType, on_delete=models.CASCADE, related_name='t_options', null=True, blank=True)
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    
    # Артикул
    option_sku = models.CharField(max_length=350, null=True, blank=True)
    # значение опции. Например #F64E60
    option_value = models.CharField(max_length=250)
    # Вес позиции
    option_weight = models.CharField(max_length=250, null=True, blank=True)
    # Количество товара с опцией. Необязательное значение
    option_stock = models.PositiveIntegerField(null=True, blank=True)
    # Наценка
    option_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Вычитать со склада. Если количество не указано - автоматически False
    option_subtract = models.BooleanField(default=False)
    # Включить изображения
    image_status = models.BooleanField(default=False)

    def get_price_after_discount(self):

        option_price = self.option_price

        
        persent = self.parent.get_sale()

        if not persent:
            return option_price
        else:
            res = option_price - (option_price * math.ceil(persent) / 100)

            return res


       


    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name = 'Опция товара'
        verbose_name_plural = 'Опции товаров'


class OptionImage(models.Model):
    parent = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name='images')
    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'products/option/images/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    src = models.ImageField(upload_to=get_image_upload_path)
    class Meta:
        verbose_name = 'Изображение опции товаров'
        verbose_name_plural = 'Изображения опций товаров'


class AutoFieldOptions(models.Model):
    
    value = models.CharField(max_length=250, verbose_name='Значение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    weight = models.CharField(max_length=250, verbose_name='Вес', null=True, blank=True)

    parent = models.ForeignKey(OptionType, on_delete=models.CASCADE, related_name='autofield', verbose_name='Опция')


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Автоопция'
        verbose_name_plural = 'Автоопции'



class CharGroup(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Группа характеристик'
        verbose_name_plural = 'Группы характеристик'


class CharName(models.Model):
    group = models.ForeignKey(CharGroup, on_delete=models.SET_NULL, related_name='g_chars', null=True, blank=True)
    text_name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.text_name

    class Meta:
        verbose_name = 'Наименование характеристики'
        verbose_name_plural = 'Наименования характеристик'


class ProductChar(models.Model):
    char_name = models.ForeignKey(CharName, on_delete=models.CASCADE, related_name='c_chars', null=True, blank=True)
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chars')
    char_value = models.TextField()

    def __str__(self):
        return self.char_name





class Combo(models.Model):
    external_id = models.CharField(max_length=250, null=True, blank=True, unique=True)
    name = models.CharField(max_length=350, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'products/thumb/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    thumb = models.ImageField(upload_to=get_image_upload_path, verbose_name='Основное изображение', null=True, blank=True)
    
    def get_thumb_mini(self):
        res = None
        setup = ShopSetup.objects.get()
        try:
            if setup.min_height and not setup.min_width:
                res = get_thumbnail(self.thumb, f'x{setup.min_height}', format="WEBP", crop='center', quality=100)
            elif setup.min_width and not setup.min_height:
                res = get_thumbnail(self.thumb, f'{setup.min_width}x', format="WEBP", crop='center', quality=100)
            elif setup.min_height and setup.min_width:
                res = get_thumbnail(self.thumb, f'{setup.min_width}x{setup.min_height}', format="WEBP", crop='center', quality=100)
            else:
                res = get_thumbnail(self.thumb, '290x193', crop='center', format="WEBP", quality=100)

            res = res.url
        except Exception as e:
            res = '/core/libs/no-image.webp'
             

        return res
    
    def get_thumb_maxi(self):
        res = None
        setup = ShopSetup.objects.get()
        try:
            if setup.max_height and not setup.max_width:
                res = get_thumbnail(self.thumb, f'x{setup.max_height}', format="WEBP", crop='center', quality=100)
            elif setup.max_width and not setup.max_height:
                res = get_thumbnail(self.thumb, f'{setup.max_width}x', format="WEBP", crop='center', quality=100)
            elif setup.max_height and setup.max_width:
                res = get_thumbnail(self.thumb, f'{setup.max_width}x{setup.max_height}', format="WEBP", crop='center', quality=100)
            else:
                res = get_thumbnail(self.thumb, '750x500', crop='center', format="WEBP", quality=100)

            res = res.url
        except:
            res = '/core/libs/no-image.webp'

        
        return res


class ComboItem(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='combo_items')
    cat = models.CharField(max_length=250, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Наценка')





# Скидка на товары и категории
class ProductSale(models.Model):
    name = models.CharField(max_length=250)

    date_start = models.DateField(null=True, blank=True, verbose_name='Дата начала акции')
    date_end = models.DateField(null=True, blank=True, verbose_name='Дата окончания акции')
    time_start = models.TimeField(null=True, blank=True, verbose_name='Время начала действия скидки', default='00:00')
    time_end = models.TimeField(null=True, blank=True, verbose_name='Время окончания действия скидки', default='23:59')

    percent = models.PositiveIntegerField(verbose_name='Процент скидки')
    rounding_up = models.BooleanField(default=True, verbose_name='Округление цены в большую сторону')

    categorys = models.ManyToManyField(Category, blank=True, related_name='sale')
    products = models.ManyToManyField(Product, blank=True, related_name='sale')

    


class FoodConstructor(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    image = models.ImageField(upload_to='constructors', verbose_name='Изображение', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    weight = models.CharField(max_length=250, verbose_name='Вес', null=True, blank=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='constructors', null=True, blank=True, verbose_name='Категория')
    btn_text = models.CharField(max_length=250, default='Собрать', verbose_name='Текст кнопки', null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name='Заголовок h1') 
    meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name='Заголовок meta title')
    meta_description = models.TextField(null=True, blank=True, verbose_name='Описание meta')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='Ключевые слова')

    slug = models.SlugField(unique=True, max_length=250)


    def get_thumb_mini(self):
        res = None
        setup = ShopSetup.objects.get()
        try:
            if setup.min_height and not setup.min_width:
                res = get_thumbnail(self.image, f'x{setup.min_height}', format="WEBP", crop='center', quality=100)
            elif setup.min_width and not setup.min_height:
                res = get_thumbnail(self.image, f'{setup.min_width}x', format="WEBP", crop='center', quality=100)
            elif setup.min_height and setup.min_width:
                res = get_thumbnail(self.image, f'{setup.min_width}x{setup.min_height}', format="WEBP", crop='center', quality=100)
            else:
                res = get_thumbnail(self.image, '290x193', crop='center', format="WEBP", quality=100)

            res = res.url
        except Exception as e:
            res = '/core/libs/no-image.webp'
             

        return res
    
    def get_thumb_maxi(self):
        res = None
        setup = ShopSetup.objects.get()
        try:
            if setup.max_height and not setup.max_width:
                res = get_thumbnail(self.image, f'x{setup.max_height}', format="WEBP", crop='center', quality=100)
            elif setup.max_width and not setup.max_height:
                res = get_thumbnail(self.image, f'{setup.max_width}x', format="WEBP", crop='center', quality=100)
            elif setup.max_height and setup.max_width:
                res = get_thumbnail(self.image, f'{setup.max_width}x{setup.max_height}', format="WEBP", crop='center', quality=100)
            else:
                res = get_thumbnail(self.image, '750x500', crop='center', format="WEBP", quality=100)

            res = res.url
        except:
            res = '/core/libs/no-image.webp'

        
        return res


    def __str__(self):
        return self.name



class ConstructorCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    image = models.ImageField(upload_to='constructors', verbose_name='Изображение', null=True, blank=True)
    parent = models.ForeignKey(FoodConstructor, on_delete=models.CASCADE, related_name='constructor_categorys', null=True, blank=True, verbose_name='Конструктор')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    obligatory = models.BooleanField(default=True, verbose_name='Категория, выбор ингридиента в которой обязателен ')
    viev_desc_in_constructor = models.BooleanField(default=False, verbose_name='Отображать описание в конструкторе')
    weight_plus = models.BooleanField(default=False, verbose_name='Добавлять вес ингридиента к конечному весу')
    show_name = models.BooleanField(default=True, verbose_name='Отображать название категории')

    CATEGORY_CLASS = (
     
    #    ('radio', 'Переключатель'),
       ('checkbox', 'Флажки'),
       ('select', 'Переключатель'),
      
    )
    

    category_class = models.CharField(max_length=250, null=True, blank=True, choices=CATEGORY_CLASS, verbose_name='Класс категории')

    minimum = models.PositiveIntegerField(null=True, blank=True, verbose_name='Минимальное количество ингридиентов можно выбрать')
    maximum = models.PositiveIntegerField(null=True, blank=True, verbose_name='Максимальное количество ингридиентов можно выбрать')

    def __str__(self):
        return self.name
    


class Ingridients(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='ingridients', verbose_name='Изображение', null=True, blank=True)
    weight = models.CharField(max_length=250, verbose_name='Вес', null=True, blank=True)
    parent = models.ForeignKey(ConstructorCategory, on_delete=models.CASCADE, related_name='ingridients', null=True, blank=True, verbose_name='Категория')
    not_ingridient = models.ManyToManyField('self', blank=True, related_name='not_category', verbose_name='Не активен при выборе ингридиента')
    extra_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Дополнительная наценка на другие ингридиенты')

    def __str__(self):
        name = self.name + ' - ' + self.parent.name + ' - ' + self.parent.parent.name
        return name
    
    def get_thumb_maxi(self):
        res = None
        try:    
            res = get_thumbnail(self.image, '750x500', crop='center', format="WEBP", quality=100)
            res = res.url

        except:
            res = ''

        
        return res
    
    def get_thumb_mini(self):
        res = None
        try:    
            res = get_thumbnail(self.image, '90x90', crop='center', format="WEBP", quality=100)
            res = res.url

        except:
            res = ''

        
        return res