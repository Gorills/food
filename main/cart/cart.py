from decimal import Decimal
from django.conf import settings
from shop.models import Product, Product, ShopSetup
from coupons.models import Coupon

try:
    price_delivery = ShopSetup.objects.get().price_delivery
    free_delivery = ShopSetup.objects.get().free_delivery
except:
    price_delivery = 0
    free_delivery = 0

class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        # сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')

        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                    'price': str(product.price),
                                    
                                    }

        if product.subtract == True:

            if product.stock <= self.cart[product_id]['quantity'] + quantity:
                quantity = product.stock     
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity

        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def minus(self, product, quantity, update_quantity=False):
        
        product_id = str(product.id)
       
        self.cart[product_id]['quantity'] -= quantity

        if self.cart[product_id]['quantity'] == 0:
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

        self.save()


    def plus(self, product, quantity, update_quantity=False):
        
        product_id = str(product.id)
        if product.subtract == True:
            if product.stock < self.cart[product_id]['quantity'] + quantity:
                quantity = product.stock     
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += 1
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()
       

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = (item['price']) * item['quantity']
           

            yield item


    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())


    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_delivery(self):
        if Decimal(self.get_total_price()) >= Decimal(free_delivery):
            summ = Decimal(0)
            return summ
        else:
            return price_delivery

    def get_free(self):
        
        return free_delivery

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount() + self.get_delivery()