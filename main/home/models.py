from django.db import models
from django.urls import reverse
from admin.singleton_model import SingletonModel
# Create your models here.

class SliderSetup(SingletonModel):

    nav = models.BooleanField(default=True, verbose_name='Включить стрелки')
    dots = models.BooleanField(default=True, verbose_name='Включить точки')
    autoplay = models.BooleanField(default=True, verbose_name='Автолистание')
    speed = models.CharField(max_length=250, default=5000, verbose_name='Скорость автопролистывания (ms)')



class Slider(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='Заголовок (не обязательно)')
    image = models.FileField(upload_to='slider', verbose_name='Изображение/видео')
    image_mob = models.FileField(upload_to='slider', verbose_name='Изображение/видео для мобильного', null=True, blank=True)
    text = models.TextField(null=True, blank=True, verbose_name='Текст (не обязательно)')
    button_text = models.CharField(max_length=250, null=True, blank=True, verbose_name='Текст кнопки (не обязательно)')
    link = models.CharField(max_length=250, null=True, blank=True, verbose_name='Ссылка (не обязательно)')
    DAY_CLASS = (
       (7, 'Все дни'),
       (0, 'Понедельник'),
       (1, 'Вторник'),
       (2, 'Среда'),
       (3, 'Четверг'),
       (4, 'Пятница'),
       (5, 'Суббота'),
       (6, 'Воскресенье'),
    )
    day = models.PositiveIntegerField(default=7, verbose_name='День недели для показа', choices=DAY_CLASS)

    def __str__(self):
        return self.name
    

    def file_format(self):
        video = [
            'webm',
            'mp4',
            'ogv',
            'ogg',
            'mpg',
            'mp2',
            'mp3',
            'wav',
            'aac',
            'flac',
            'aiff',
            'wma',
        ]
        photo = [
            'jpg',
            'jpeg',
            'png',
            'gif',
            'bmp',
            'tif',
            'tiff',
            'psd',
            'ico',
            'webp',
        ]
        format = self.image.url.split('.')[-1]

        if format in video:
            return 'video'
        elif format in photo:
            return 'photo'

        

    class Meta:
       
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'



class Page(models.Model):
    
    status = models.BooleanField(default=True, verbose_name='Включить')
    top_link = models.BooleanField(default=True, verbose_name='Ссылка в хедере')
    bottom_link = models.BooleanField(default=True, verbose_name='Ссылка в футере')
    PAGE_CLASS = (
       ('o-nas', 'О нас'),
       ('oplata', 'Оплата'),
       ('politic', 'Политика конфиденциальности'),
       ('dostavka', 'Доставка'),
       ('kontakty', 'Контакты'),
       ('kak-zakazat', 'Как заказать'),
       ('skidki-i-bonusy', 'Скидки и бонусы'),
       ('vozvrat-tovarov', 'Возврат товаров'),
    )
    type = models.CharField(max_length=200, choices=PAGE_CLASS, verbose_name='Тип страницы', unique=True)
    name = models.CharField(max_length=350, null=True, blank=True, verbose_name='Название страницы')
    meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name='h1')
    text = models.TextField(verbose_name='Текст страницы')
    meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name='Мета тайтл')
    meta_description = models.TextField(null=True, blank=True, verbose_name='Мета описание')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='Ключевые слова через запятую')
    image = models.ImageField(upload_to='catalog', null=True, blank=True, verbose_name='Изображение')
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("page_detail", kwargs={"slug": self.type})
    

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'


# class PageBlock(models.Model):
#     parent = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_blocks', verbose_name='Страница')
#     children = models.OneToOneField('Block', on_delete=models.CASCADE, related_name='block_page', verbose_name='Блок')
#     sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
#     top = models.BooleanField(default=True, verbose_name='Над основным текстом')
#     bottom = models.BooleanField(default=True, verbose_name='Под основным текстом')


# class Block(models.Model):
#     name = models.CharField(max_length=250)
#     BLOCK_CLASS = (
#        ('slider', 'Слайдер'),
#        ('banner', 'Баннер'),
#        ('call_to_action', 'Призыв к действию'),
#     )
#     block_class = models.CharField(max_length=200, choices=BLOCK_CLASS, verbose_name='Тип блока')
#     home = models.BooleanField(default=False, verbose_name='Отображать на главной странице')
#     sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

#     title = models.CharField(max_length=450, verbose_name='Заголовок', null=True, blank=True)
#     text = models.TextField(verbose_name='Текст блока', null=True, blank=True)
#     button_text = models.CharField(max_length=250, null=True, blank=True)
#     background = models.ImageField(upload_to='block/backgropund', null=True, blank=True)

#     def __str__(self):
#         return self.name