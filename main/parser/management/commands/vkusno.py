from django.core.management.base import BaseCommand
from parser.vkusno import parse_vkusnoitochka, delete_products


category_urls = {
    'Сеты и пары': 'https://vkusnoitochka.ru/menu/sety-i-pary',
    'Напитки': 'https://vkusnoitochka.ru/menu/napitki',
    'Картофель, стартеры и салаты': 'https://vkusnoitochka.ru/menu/kartofel-startery-i-salaty',
    'Кафе': 'https://vkusnoitochka.ru/menu/kafe',
    'Завтрак': 'https://vkusnoitochka.ru/menu/zavtrak',
    'Кидз Комбо': 'https://vkusnoitochka.ru/menu/kidz-kombo',
    'Десерты': 'https://vkusnoitochka.ru/menu/deserty_2',
    'Соусы': 'https://vkusnoitochka.ru/menu/sousy'
}

class Command(BaseCommand):
    help = 'Синхронизация каталогов с IIKO'
    def handle(self, *args, **kwargs):
        delete_products()
        parse_vkusnoitochka(
            category_urls=category_urls,
            product_class='product-card',     # Класс карточки товара
            name_class='product-card__title', # Класс имени товара
            price_class='font-bold',          # Класс цены товара
            image_class='common-image__img'   # Класс изображения товара
        )
      