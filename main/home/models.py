from django.db import models
from django.urls import reverse
from admin.singleton_model import SingletonModel
# Create your models here.
from main.transliterate_filename import transliterate_file
from django.utils import timezone
from sorl.thumbnail import get_thumbnail

class SliderSetup(SingletonModel):

    nav = models.BooleanField(default=True, verbose_name='Включить стрелки')
    dots = models.BooleanField(default=True, verbose_name='Включить точки')
    autoplay = models.BooleanField(default=True, verbose_name='Автолистание')
    speed = models.CharField(max_length=250, default=5000, verbose_name='Скорость автопролистывания (ms)')
    full_screen = models.BooleanField(default=True, verbose_name='Включить полноэкранный режим')
    height = models.CharField(max_length=250, default=600, verbose_name='Высота слайдера')
    height_mob = models.CharField(max_length=250, default=250, verbose_name='Высота слайдера для мобильного')
    title_size = models.CharField(max_length=250, default=56, verbose_name='Размер шрифта заголовка')
    title_size_mob = models.CharField(max_length=250, default=36, verbose_name='Размер шрифта заголовка для мобильного')
    desc_size = models.CharField(max_length=250, default=24, verbose_name='Размер шрифта описания')
    desc_size_mob = models.CharField(max_length=250, default=18, verbose_name='Размер шрифта описания для мобильного')
    text_max_width = models.CharField(max_length=250, default=700, verbose_name='Максимальная ширина текста')

    TEXT_CHOISE = (
        ('start', 'Слева'),
        ('center', 'По центру'),
        ('end', 'Справа'),
    )

    text_align = models.CharField(max_length=250, default='center', choices=TEXT_CHOISE, verbose_name='Выравнивание текста')
    image_compression = models.PositiveIntegerField(blank=True, null=True, default=1, verbose_name='Качество изображения')


class Slider(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='Заголовок (не обязательно)')
    text_color = models.CharField(max_length=250, null=True, blank=True, verbose_name='Цвет текста (не обязательно)')
    
    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'slider/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    

    image = models.FileField(upload_to=get_image_upload_path, verbose_name='Изображение/видео')
    image_opacity = models.PositiveIntegerField(default=100, verbose_name='Непрозрачность изображения')
    bg = models.CharField(max_length=250, null=True, blank=True, default='#FFFFFF', verbose_name='Цвет фона (не обязательно)')
    image_mob = models.FileField(upload_to=get_image_upload_path, verbose_name='Изображение/видео для мобильного', null=True, blank=True)
    text = models.TextField(null=True, blank=True, verbose_name='Текст (не обязательно)')
    button_text = models.CharField(max_length=250, null=True, blank=True, verbose_name='Текст кнопки (не обязательно)')
    link = models.CharField(max_length=250, null=True, blank=True, verbose_name='Ссылка (не обязательно)')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
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
    show = models.BooleanField(default=True, verbose_name='Показывать')

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

    def get_image_max(self):
        setup = SliderSetup.objects.first()
        height = setup.height
        width = 1920
        image_compression = setup.image_compression
        res = get_thumbnail(self.image, f'x{int(height) * image_compression}', format="WEBP", crop='center', quality=100)
        return res
    
    def get_image_mob(self):
        setup = SliderSetup.objects.first()
        height = setup.height_mob
        width = 560
        image_compression = setup.image_compression
        res = get_thumbnail(self.image_mob, f'x{int(height) * image_compression}', format="WEBP", crop='center', quality=100)
        return res

    class Meta:
       
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'



class Page(models.Model):
    
    status = models.BooleanField(default=True, verbose_name='Включить')
    top_link = models.BooleanField(default=True, verbose_name='Ссылка в хедере')
    bottom_link = models.BooleanField(default=True, verbose_name='Ссылка в футере')
    PAGE_CLASS = (
       ('o-nas', 'О нас'),
       ('bron-stolika', 'Бронь столика'),
       ('oplata', 'Оплата и доставка'),
       ('otzivi', 'Отзывы'),
       ('politic', 'Политика конфиденциальности'),
      
       ('kontakty', 'Контакты'),
       
       ('skidki-i-bonusy', 'Скидки и бонусы'),
       
    )
    type = models.CharField(max_length=200, choices=PAGE_CLASS, verbose_name='Тип страницы', unique=True)
    name = models.CharField(max_length=350, null=True, blank=True, verbose_name='Название страницы')
    meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name='h1')
    text = models.TextField(verbose_name='Текст страницы')
    meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name='Мета тайтл')
    meta_description = models.TextField(null=True, blank=True, verbose_name='Мета описание')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='Ключевые слова через запятую')
    code = models.TextField(null=True, blank=True, verbose_name='Дополнтельный код')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def get_image_upload_path(instance, filename):
        """
        Function to specify the upload path for the image
        """
        folder = 'catalog/'  # Fixed folder name
        return f"{folder}{transliterate_file(instance, filename)}"
    
    
    image = models.ImageField(upload_to=get_image_upload_path, null=True, blank=True, verbose_name='Изображение')
    
    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("page_detail", kwargs={"slug": self.type})
    

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'



class PageItem(models.Model):

    ITEM_CLASS = (
        ('time', 'Время доставки'),
        ('srok', 'Сроки доставки'),
        ('time_to_drive', 'Время в пути'),
        ('info', 'Дополнительная информация'),
    )

    item_type = models.CharField(max_length=250, verbose_name='Тип блока', choices=ITEM_CLASS, null=True, blank=True)

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_item', verbose_name='Страница')
    image = models.FileField(upload_to='page', verbose_name='Изображение', null=True, blank=True)

    text = models.TextField(verbose_name='Текст')


class PlaceImages(models.Model):
    
    image = models.ImageField(upload_to='place', verbose_name='Изображение зала')







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
    

import random
class Reviews(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    text = models.TextField(verbose_name='Текст отзыва')
    scores = models.PositiveIntegerField(default=0, verbose_name='Оценка')
    date = models.DateField(verbose_name='Дата отзыва')
    link = models.CharField(max_length=250, null=True, blank=True, verbose_name='Ссылка на отзыв (не обязательно)')
    image = models.ImageField(upload_to='reviews', null=True, blank=True, verbose_name='Изображение (не обязательно)')

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='reviews', verbose_name='Страница')
    view_home = models.BooleanField(default=True, verbose_name='Отображать на главной странице')
    status = models.BooleanField(default=True, verbose_name='Активный')


    REVIEW_CLASS = (
        ('2gis', '2gis'),
        ('yandex', 'yandex'),

    )
    platform = models.CharField(max_length=200, choices=REVIEW_CLASS, verbose_name='Тип отзыва')



    bg_color = models.CharField(max_length=200, null=True, blank=True, verbose_name='Цвет')

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        # Здесь можно добавить логику выбора цвета в зависимости от каких-то условий
        # Например, можно использовать случайный выбор из списка цветов
        color_list = [
            '#FBCEB1', 
            '#FDD9B5', 
            '#B5B8B1', 
            '#7FFFD4', 
            '#78DBE2', 
            '#E32636', 
            '#AB274F', 
            '#E52B50',
            '#ffdecf',
            '#ba7967',
            '#5e6f64',
            '#3f4441',
            '#ff9a76',
            '#679b9b',
            '#8d93ab',
            '#16213e',
            '#ff847c',
            '#99b898',
            '#ee6f57',
            '#836f6f',
            '#bbd196',
            '#ababcb',
            
            ]

        if not self.bg_color:
            self.bg_color = random.choice(color_list)

        super().save(*args, **kwargs)