from bs4 import BeautifulSoup
import requests
from django.db import models
from pytils.translit import slugify
from django.core.files import File
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from decimal import Decimal, InvalidOperation
import os
from urllib.parse import urljoin

from shop.models import Product, Category

# Функция для очистки товаров перед парсингом
def delete_products():
    category = Category.objects.filter(name='Вкусно и точка').delete()

# Функция для создания уникального slug
def generate_unique_slug(name, model):
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug



# Функция для парсинга категорий и товаров с сайта "Вкусноиточка"
def parse_vkusnoitochka(category_urls, product_class, name_class, price_class, image_class):
    # Настройка Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 25)  # Ожидание загрузки элементов

    parent, _ = Category.objects.get_or_create(
        name='Вкусно и точка',
        defaults={
            'slug': 'vkusnoitochka',
            'top': True,
            'home': True
            }
    )
    
    try:
        for category_name, category_url in category_urls.items():
            driver.get(category_url)
            time.sleep(2)  # Задержка для загрузки динамических товаров
            
            category_slug = generate_unique_slug(category_name, Category)
            print(f"Найдена категория: {category_name}", slugify(category_name))
            
            # Сохранение категории в базу данных
            category, created = Category.objects.get_or_create(name=category_name, defaults={'slug': category_slug, 'top': False, 'parent': parent})
            if not created:
                # Обновление slug для существующей категории, если он пустой
                if not category.slug:
                    category.slug = category_slug
                    category.save()
                print(f"Категория с названием '{category_name}' уже существует, загрузка товаров.")
            
            # Парсинг товаров в категории
            product_elements = driver.find_elements(By.CSS_SELECTOR, f"a.{product_class.replace(' ', '.')}")
            
            for product_element in product_elements:
                # Получение имени товара
                product_name = product_element.find_element(By.CLASS_NAME, name_class).text.strip()
                print(f"Найден товар: {product_name}")

                # Получение цены товара
                try:
                    price_element = product_element.find_element(By.CLASS_NAME, price_class)
                    product_price_raw = price_element.text.strip()
                    product_price = re.sub(r'[^\d,\.]', '', product_price_raw).replace(',', '.')
                    try:
                        product_price = Decimal(product_price)
                    except InvalidOperation:
                        product_price = None
                    print(f"Цена товара: {product_price}")
                except NoSuchElementException:
                    product_price = None
                    print(f"Товар '{product_name}' без указанной цены.")



                # Создание или обновление товара в базе данных
                product_slug = generate_unique_slug(product_name, Product)
                print(f"Создание или обновление товара: {product_name} ({slugify(product_name)})")
                product, created = Product.objects.get_or_create(name=product_name, defaults={'price': product_price, 'parent': category, 'slug': product_slug})
                if not created:
                    product.price = product_price
                    product.parent = category
                    
                    product.save()
                    print(f"Обновлена цена для товара '{product_name}'")
                
                # Получение изображения товара, если товар новый
                if created:
                    try:
                        image_element = product_element.find_element(By.CLASS_NAME, image_class)
                        image_url = image_element.get_attribute('src')
                        image_name = os.path.basename(image_url)
                        image_path = os.path.join('media', 'products', image_name)
                        response = requests.get(image_url, stream=True)
                        if response.status_code == 200:
                            with open(image_path, 'wb') as f:
                                for chunk in response.iter_content(1024):
                                    f.write(chunk)
                        print(f"Скачано изображение: {image_name}")
                        with open(image_path, 'rb') as img_file:
                            product.thumb.save(image_name, File(img_file), save=True)
                    except NoSuchElementException:
                        print(f"Изображение для товара '{product_name}' не найдено.")
    except Exception as e:
        print(f"Не удалось найти элементы на странице: {e}")
    finally:
        driver.quit()

# Пример использования
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

# delete_products()
# parse_vkusnoitochka(
#     category_urls=category_urls,
#     product_class='product-card',     # Класс карточки товара
#     name_class='product-card__title', # Класс имени товара
#     price_class='font-bold',          # Класс цены товара
#     image_class='common-image__img'   # Класс изображения товара
# )