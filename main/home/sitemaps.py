from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.utils import timezone


from shop.models import Category, Product
from .models import Page


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'home',
            'catalog'
            ]
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        # Замените эту строку на логику получения даты модификации для каждой страницы
        # Ниже пример с использованием текущей даты и времени
        if item == 'home':
            # Ваша логика для страницы 'home'
            return timezone.now()
        if item == 'catalog':
            # Ваша логика для страницы 'home'
            return timezone.now()
        
    def priority(self, item):
        if item == 'home':
            # Приоритет для страницы 'home'
            return 1.0
        if item == 'catalog':
            # Приоритет для страницы 'home'
            return 0.8

    
class PageSitemap(Sitemap):
    def items(self):
        return Page.objects.filter(status=True)

    def lastmod(self, item):
        return item.updated_at
    
    def priority(self, item):
        return 0.8
    
class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.filter(status=True)

    def lastmod(self, item):
        return item.update_at

    def priority(self, item):
        return 0.8
    
class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.filter(status=True)

    def lastmod(self, item):
        return item.update_at
    
    def priority(self, item):
        return 0.6