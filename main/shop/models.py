from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from admin.singleton_model import SingletonModel
# Create your models here.


class ShopSetup(SingletonModel):
    STATUS_CLASS = (
       ('hide', 'Скрыть'),
       ('out_of_stock', 'Статус: нет в налчии'),
       ('to_order', 'Статус: под заказ'),
    )
    start_delivery = models.PositiveIntegerField(default=10, verbose_name='Время начала доставки')
    end_delivery = models.PositiveIntegerField(default=21, verbose_name='Время окончания доставки')
    delay = models.PositiveIntegerField(default=2, verbose_name='Задержка при формировании заказа на доставку. Считается так: текущее время + время задержки')
    
    status = models.CharField(max_length=250, verbose_name='Товар при 0 остатке', choices=STATUS_CLASS, default='out_of_stock')
    description = models.TextField(null=True, blank=True, verbose_name='Описание каталога')
    meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name='h1')
    meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name='Мета тайтл')
    meta_description = models.TextField(null=True, blank=True, verbose_name='Мета описание')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='Ключевые слова через запятую')
    image = models.ImageField(upload_to='catalog', null=True, blank=True, verbose_name='Изображение')
    action = models.BooleanField(default=True, verbose_name='Включить акции')
    new_products = models.BooleanField(default=True, verbose_name='Включить новинки')
    sales_hits = models.BooleanField(default=True, verbose_name='Включить хиты продаж')



class Category(models.Model):
    name = models.CharField(max_length=350)
    description = models.TextField(null=True, blank=True)
    meta_h1 = models.CharField(max_length=350, null=True, blank=True)
    meta_title = models.CharField(max_length=350, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='catalog', null=True, blank=True)
    top = models.BooleanField()
    column = models.PositiveIntegerField(default=1)
    sort_order = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, max_length=250)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

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
    image = models.ImageField(upload_to='manufacturer', null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0, null=True, blank=True)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)




    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'



class Product(models.Model):
    # Выводить в меню и других списках
    name = models.CharField(max_length=350)
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
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

    slug = models.SlugField(unique=True, max_length=250)

    # Дата поступления
    date_available = models.DateField(auto_now_add=True)

    # Настройка параметров товара
    length = models.CharField(max_length=200, null=True, blank=True)
    width = models.CharField(max_length=200, null=True, blank=True)
    height = models.CharField(max_length=200, null=True, blank=True)

    # color = models.CharField(max_length=250, null=True, blank=True)
    # color_name = models.CharField(max_length=250, null=True, blank=True)

    # Состав
    # composition = models.TextField(null=True, blank=True)

    LENGHT_CLASS = (
       ('см', 'Сантиметры'),
       ('мм', 'Миллиметры'),
    )
    length_class = models.CharField(max_length=200, choices=LENGHT_CLASS, default='sm',)
    weight = models.CharField(max_length=200, null=True, blank=True)
    WEIGHT_CLASS = (
       ('кг', 'Киллограмы'),
       ('гр', 'Граммы'),
    )
    weight_class = models.CharField(max_length=200, choices=WEIGHT_CLASS, default='kg',)

    # Связи
    product_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='manufacturer_products', null=True, blank=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    # Связанные товары
    product_connect = models.ManyToManyField('self', related_name='connects', blank=True)

    # Маленькое изображение
    thumb = models.ImageField(upload_to='products/thumb')

    # Показывать/не показывать. Возможность скрыть товар
    status = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)    

    def __str__(self):
        try:
            name = self.name + ', ' + self.color_name
        except:
            name = self.name
        return name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"parent": self.parent.slug, "slug": self.slug})
    
    def get_sale(self):
        old = self.old_price
        new = self.price
        razn = old - new
        persent = (razn/old)*100
        return persent

        

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    src = models.ImageField(upload_to='products/images')
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'



class OptionType(models.Model):
    OPTION_CLASS = (
     
       ('radio', 'Переключатель'),
       ('radio', 'Переключатель'),
      
    )
    name = models.CharField(max_length=250)
    option_class = models.CharField(max_length=200, choices=OPTION_CLASS, default='radio')

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
    # Количество товара с опцией. Необязательное значение
    option_stock = models.PositiveIntegerField(null=True, blank=True)
    # Наценка
    option_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Вычитать со склада. Если количество не указано - автоматически False
    option_subtract = models.BooleanField(default=False)
    # Включить изображения
    image_status = models.BooleanField(default=False)

    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name = 'Опция товара'
        verbose_name_plural = 'Опции товаров'


class OptionImage(models.Model):
    parent = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name='images')
    src = models.ImageField(upload_to='products/option/images')
    class Meta:
        verbose_name = 'Изображение опции товаров'
        verbose_name_plural = 'Изображения опций товаров'



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