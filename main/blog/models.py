from django.db import models
from django.urls import reverse
from admin.singleton_model import SingletonModel
# Create your models here.


class BlogSetup(SingletonModel):
    description = models.TextField(null=True, blank=True, verbose_name='Описание каталога')
    meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name='h1')
    meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name='Мета тайтл')
    meta_description = models.TextField(null=True, blank=True, verbose_name='Мета описание')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='Ключевые слова через запятую')
    image = models.ImageField(upload_to='catalog', null=True, blank=True, verbose_name='Изображение')


class BlogCategory(models.Model):
    name = models.CharField(max_length=250)
    meta_h1 = models.CharField(max_length=350, null=True, blank=True)
    meta_title = models.CharField(max_length=350, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog', null=True, blank=True)

    slug = models.SlugField(unique=True, max_length=250)

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog_category_detail", kwargs={"slug": self.slug})

    class Meta:
        
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'
    


class Post(models.Model):
    parent = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)

    name = models.CharField(max_length=250)

    meta_h1 = models.CharField(max_length=350, null=True, blank=True)
    meta_title = models.CharField(max_length=350, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog', null=True, blank=True)

    slug = models.SlugField(unique=True, max_length=250)

    draft = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name

    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"parent": self.parent.slug, 'slug': self.slug})
    

    class Meta:
        
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class PostBlock(models.Model):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blocks')
    type = models.CharField(max_length=250)
    title = models.CharField(max_length=400, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog/images', null=True, blank=True)
    video = models.FileField(upload_to='blog/video',null=True, blank=True)
    order = models.PositiveIntegerField(default=0)