# Проект food

## Стек

- **Backend:** Python, **Django 3.2** (`requirements.txt` в корне репозитория).
- **API:** Django REST Framework 3.14.
- **Аутентификация:** django-allauth 0.51.
- **Контент:** CKEditor, sorl-thumbnail, django-cleanup.
- **Платежи:** YooKassa и др. (см. `pay/`, `requirements.txt`).
- **Интеграции:** iiko (`integrations/`), Telegram (telepot), SMS, внешние службы доставки.
- **Frontend сборка (исторически):** Node/Yarn/Gulp/BEM — см. корневой `README.md` (шаблон gulp-scss-starter); статика и темы лежат в `main/core/theme/` и связанных путях.

## Структура

| Путь | Назначение |
|------|------------|
| `main/manage.py` | Точка входа Django |
| `main/main/` | Проект Django: `settings.py`, корневой `urls.py`, WSGI, `local_settings`, whitenoise |
| `main/core/` | Общие шаблоны тем, статика, JS/CSS по темам (`fast_theme`, `flowers_light`, `sushi`, …) |
| `main/shop/` | Каталог, товары, модели витрины |
| `main/cart/` | Корзина, расчёт цен, доставки, купоны/лояльность |
| `main/orders/` | Оформление и обработка заказов, уведомления |
| `main/api/` | REST API v1 |
| `main/pay/` | Платежи |
| `main/delivery/` | Доставка и зоны |
| `main/integrations/` | Внешние системы (iiko и др.) |
| `main/accounts/` | Пользователи, профили, лояльность (частично через allauth) |
| `main/admin/` | Кастомная админка (не `django.contrib.admin` из коробки) |
| `main/home/` | Публичные страницы, CMS-страницы, `handler404` |
| `main/setup/` | Настройки темы/сайта |
| `main/subdomains/` | Поддомены |
| `main/qr_menu/` | QR-меню |
| `main/blog/`, `main/coupons/`, `main/yafeed/`, `main/sms/`, `main/actions/` | Тематические приложения |

Каталог `#src/` в репозитории — префикс в именах некоторых путей (шаблоны/ассеты), не отдельный пакет Python.

## Точки входа

- **URL:** `main/main/urls.py` — монтирует `cart`, `orders`, `catalog` (`shop`), `blog`, кастомный `admin`, `accounts`, `api/v1/`, `delivery`, `qr_menu`, в конце `home` (в т.ч. catch-all для страниц).
- **Настройки:** `main/main/settings.py` + `main/main/local_settings.py` (секреты и окружение; не коммитить реальные ключи).

## Соглашения

- Приложения — пакеты под `main/<app>/` с типичным Django-раскладом (`models`, `views`, `urls`, `migrations` в `.gitignore` по политике репозитория).
- Кросс-импорты доменных моделей между `orders`, `cart`, `shop`, `pay`, `setup`, `accounts`, `integrations` — ожидаемы; менять контракты осторожно.
- Тема оформления выбирается через `setup` / `ThemeSettings` (см. паттерн в `orders.views`).

## Ограничения

- Django 3.2 LTS — при обновлении мажорной версии нужна отдельная ветка и тесты.
- Секреты только через `local_settings` / переменные окружения (не хардкодить в чате и в публичных ветках).
- `migrations` в `.gitignore` — миграции могут не отслеживаться; уточнять у команды перед изменением схемы БД.
