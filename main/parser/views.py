from bs4 import BeautifulSoup
import requests
from django.db import models
import os
from urllib.parse import urljoin
from django.core.files import File
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

from shop.models import Product, ProductOption, ProductChar, Category

# Функция для очистки товаров перед парсингом
def delete_products():
    Product.objects.all().delete()
    ProductOption.objects.all().delete()
    ProductChar.objects.all().delete()
    Category.objects.all().delete()

# Функция для парсинга динамически загружаемой HTML страницы с использованием Selenium
def parse_page_with_selenium(url, product_class, name_class, price_class, category_class):
    # Настройка Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    wait = WebDriverWait(driver, 15)  # Ожидание загрузки элементов
    
    try:
        # Ожидание загрузки всех товаров на странице
        product_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"a.{product_class.replace(' ', '.')}")))
        for product_element in product_elements:
            retries = 3
            while retries > 0:
                try:
                    # Получение родительского элемента товара для поиска категории
                    parent_section = product_element.find_element(By.XPATH, "ancestor::div[contains(@class, 'pt-32 pb-16')]")
                    
                    # Попытка найти элемент категории
                    category_name = None
                    try:
                        category_name_element = parent_section.find_element(By.CSS_SELECTOR, f".{category_class.replace(' ', '.')}")
                        category_name = category_name_element.text.strip()
                        print(f"Найдена категория: {category_name}")
                    except NoSuchElementException as e:
                        print(f"Ошибка при получении категории: {e}")
                    
                    if category_name:
                        category, _ = Category.objects.get_or_create(name=category_name)
                    else:
                        category = None

                    # Получение имени товара
                    product_name = product_element.find_element(By.CLASS_NAME, name_class).text.strip()
                    print(f"Найден товар: {product_name}")

                    # Получение цены товара
                    price_element = product_element.find_element(By.CLASS_NAME, price_class)
                    product_price_raw = price_element.find_element(By.TAG_NAME, 'span').text.strip()
                    product_price = re.sub(r'[^\d,\.]', '', product_price_raw).replace(',', '.')
                    if not product_price:  # Пропуск товаров без цены
                        raise ValueError("Пропуск товаров без цены")
                    print(f"Цена товара: {product_price}")

                    # Переход на страницу товара для получения описания
                    product_url = product_element.get_attribute('href')
                    driver.execute_script("window.open(arguments[0]);", product_url)
                    driver.switch_to.window(driver.window_handles[-1])
                    try:
                        description_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, '_1qwyRmPDsjj')))
                        product_description = description_element.text.strip()
                        print(f"Описание товара: {product_description}")
                    except NoSuchElementException:
                        product_description = ""
                        print(f"Описание для товара '{product_name}' не найдено.")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    break
                except (StaleElementReferenceException, ValueError, NoSuchElementException) as e:
                    print(f"Ошибка при получении данных товара: {e}")
                    retries -= 1
                    if retries == 0:
                        continue

            # Создание или обновление товара в базе данных
            product, created = Product.objects.get_or_create(name=product_name, defaults={'price': product_price, 'parent': category, 'short_description': product_description})
            if not created:
                product.price = product_price
                if category:
                    product.parent = category
                product.short_description = product_description
                product.save()
    except Exception as e:
        print(f"Не удалось найти элементы продуктов на странице: {e}")
    finally:
        driver.quit()

# Пример использования
# delete_products()
# parse_page_with_selenium(
#     url='https://rostics.ru/',
#     product_class='_1ptLJr9K6ka',  # Класс карточки товара
#     name_class='_14ZQf5wtqxX',      # Класс имени товара
#     price_class='_3cJe_ZvVwfW',     # Класс цены товара
#     category_class='t-xl condensed' # Класс категории товара
# )