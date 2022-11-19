from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


from shop.models import Category, Product
from .models import Page


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'home',
     
            ]
    def location(self, item):
        return reverse(item)

    
class PageSitemap(Sitemap):
    def items(self):
        return Page.objects.filter(status=True)

    
class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.filter(status=True)

    def lastmod(self, item):
        return item.update_at


class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.filter(status=True)

    def lastmod(self, item):
        return item.update_at