from decimal import Decimal
from django.conf import settings
from shop.models import Category, Combo, ComboItem, Product, Product, ProductOption, ShopSetup, ConstructorCategory, Ingridients, FoodConstructor
from coupons.models import Coupon
from accounts.models import LoyaltyCardSettings, LoyaltyCard, UserProfile
import decimal
from delivery.models import Delivery
import math
import json

try: 
    delivery_integrations = Delivery.objects.filter(active=True).first()

except:
    delivery_integrations = None



D = decimal.Decimal

try:
    del_zones = ShopSetup.objects.get().zones_delivery
except:
    del_zones = False


try:
    price_delivery = ShopSetup.objects.get().price_delivery
    free_delivery = ShopSetup.objects.get().free_delivery
    min_delivery = ShopSetup.objects.get().min_delivery
    
except:
    price_delivery = 0
    free_delivery = 0
    min_delivery = 0

class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)


        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


        # Программа лояльности
        try:
            user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
            loyalty_card = LoyaltyCard.objects.get(user=user_profile)
            

            percent_up = loyalty_card.status().percent_up
            percent_down = loyalty_card.status().percent_down
            percent_pay = loyalty_card.status().percent_pay
            balls = loyalty_card.balls
            

        except Exception as e:
            # print(e)
            user_profile = None
            loyalty_card = None

            percent_up = 0
            percent_down = 0
            percent_pay = 0
            balls = 0

        
        self.percent_up = percent_up
        self.percent_down = percent_down
        self.percent_pay = percent_pay
        self.balls = balls


        try:
            self.active_balls = Decimal(request.session['active_balls'])
        except:
            self.active_balls = Decimal('0.00')

        
        try:
            self.first_delivery = request.session['first_delivery']
        except:
            self.first_delivery = 0
            
        # print(self.first_delivery)
        if not self.first_delivery:

            self.first_delivery = 0

        


        # сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')


        get_d = request.session.get('delivery')
        get_delivery_sum = request.session.get('delivery_summ')

        
        if not get_delivery_sum:
            self.get_delivery_sum = price_delivery
            
        else:
            self.get_delivery_sum = get_delivery_sum

        
        


        if not get_d:
            self.get_d = 1
        self.get_d = get_d

        # Сумма для бесплатной доставки
        self.free_delivery = request.session.get('free_delivery')
        if not self.free_delivery:
            self.free_delivery = Decimal(free_delivery)

        

        # Минимальная сумма для доставки
        self.min_delivery = request.session.get('min_delivery')
        if not self.min_delivery:
            
            self.min_delivery = min_delivery    
        
        

        # Пустой адрес доставки
        delivery_address = request.session.get('delivery_address')
        if not delivery_address:
            delivery_address = self.session['delivery_address'] = {
                'street': ''
               
            }
        self.delivery_address = delivery_address

        # Пустой телефон
        phone = request.session.get('phone')
        if not phone:
            phone = self.session['phone'] = {
                'phone': ''
            }
        self.phone = phone

        
        # Инициализируем пустой комбо
        combos = request.session.get('combos')
        if not combos:
            combos = self.session['combos'] = {
                '0': { 
                    'id': 0,
                    'combo': 0,
                    'quantity': 0,
                    'price': 0,
                    'products': None
                }
            }
        self.combos = combos

        # Инициализируем пустой конструктор
        constructors = request.session.get('constructors')
        if not constructors:
            constructors = self.session['constructors'] = {
                '0': { 
                    'id': 0,
                    'constructor': 0,
                    'quantity': 0,
                    'price': 0,
                    'products': None
                }
            }
        self.constructors = constructors

        # self.constructors.clear()

        # Инициализируем пустой товар с опциями
        options = request.session.get('options')
        if not options:
            options = self.session['options'] = {
                '0': { 
                    'id': '',
                    'quantity': int(0),
                    'price': str(0),
                    'products': None,
                    'options': ''
                    
                }
            }
        self.options = options


        # Перебираем все ключи и ищем товары, которые были удалены 
        product_ids = self.cart.keys()
        empty = []
        for id in product_ids:
            try:
                prod = Product.objects.get(id=id)
              
            except:
                product = id
                empty.append(product)

        # Удаляем удаленные товары из корзины
        for em in empty:
            product = str(em)
            self.remove(product)
    
    def add_options(self, options_id, options, products, quantity, price):
        self.session['active_balls'] = '0.00'
        if options_id not in self.options:
            self.options[options_id] = {
                'id': options_id,
                'quantity': int(quantity),
                'price': str(price),
                'products': products,
                'options': options
                }
        else:
            self.options[options_id]['quantity'] += int(quantity)
        self.session.modified = True
      
    def remove_options(self, options_id):
        self.session['active_balls'] = '0.00'
        if options_id in self.options:
            del self.options[options_id]
            self.save()

    def plus_options(self, options_id):
        self.session['active_balls'] = '0.00'
        
        self.options[options_id]['quantity'] += 1
        self.save()
       


    def minus_options(self, options_id):
        self.session['active_balls'] = '0.00'
        self.options[options_id]['quantity'] -= 1

        if self.options[options_id]['quantity'] == 0:
            del self.options[options_id]
        self.save()


    def options_clear(self):
        items = self.options.keys()
        for item in list(items):
            if item != 0:
                del self.options[item]
                self.save()  


    def get_options(self):
        options_list = []
        for item in self.options.values():
            try:
                product = Product.objects.get(id=str(item['products']))
                options_spisok = item['id'].split(',')
                options_res_by_type = {}

                for option in options_spisok:
                    product_option = ProductOption.objects.get(id=option, parent=product)
                    option_type = product_option.type

                    if option_type not in options_res_by_type:
                        options_res_by_type[option_type] = []

                    options_res_by_type[option_type].append(product_option)




                options_list.append({
                    'id': item['id'],
                    'quantity': int(item['quantity']),
                    'price': Decimal(item['price']),
                    'products': product,
                    'options': options_res_by_type,
                })
            except Exception as e:
                # print(e)
                pass

        return options_list

        

    def add_combo(self, combo, combo_id,  products, quantity, price):

        if combo not in self.combos:

            self.combos[combo] = {
                'combo': int(combo_id),
                'quantity': int(quantity),
                'price': str(price),
                'products': products
                
                }

        else:
            self.session['active_balls'] = '0.00'
            self.combos[combo]['quantity'] += int(quantity)
        
        self.session.modified = True




    def remove_combo(self, combo):
        self.session['active_balls'] = '0.00'
        if combo in self.combos:
            del self.combos[combo]
            self.save()

    def plus_combo(self, combo):
        self.session['active_balls'] = '0.00'
        
        self.combos[combo]['quantity'] += 1
        self.save()
       


    def minus_combo(self, combo):
        self.session['active_balls'] = '0.00'
        self.combos[combo]['quantity'] -= 1

        if self.combos[combo]['quantity'] == 0:
            del self.combos[combo]
        self.save()


    def combo_clear(self):
        items = self.combos.keys()
        for item in list(items):
            if item != 0:
                del self.combos[item]
                self.save()



    def get_combos(self):
        combo_list = []
        # combo_items = ComboItem.objects
        for item in self.combos.values():
            try:

                combo_items = []
                items_list = str(item['products']).split(',')

                for i in items_list:
                    try:
                        item_c = ComboItem.objects.get(id=str(i))
                        combo_items.append(item_c)

                    except: 
                        pass
                
                combo_get = Combo.objects.get(id=str(item['combo']))
                combo_list.append({

                    'combo':combo_get,
                    'price': Decimal(item['price']),
                    'quantity': int(item['quantity']),
                    'products': combo_items

                    })
  

            except:
                pass

            

        
        return combo_list
    
    def combo_summ(self):
        
        
        return sum((Decimal(item['price']) * item['quantity']) for item in self.combos.values())


    def options_summ(self):
        
        
        return sum((Decimal(item['price']) * item['quantity']) for item in self.options.values())

    def constructors_summ(self):
        
        return sum((Decimal(item['price']) * item['quantity']) for item in self.constructors.values())

    def count_combos(self):
        combo_len = sum(int(item['quantity']) for item in self.combos.values())
        return combo_len
    
    def count_options(self):
        combo_len = sum(int(item['quantity']) for item in self.options.values())
        return combo_len
    
    def count_constructors(self):

        constructor_len = sum(int(item['quantity']) for item in self.constructors.values())
        return constructor_len
    

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        self.session['active_balls'] = '0.00'

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': product.minimum - 1,
                                     'free': 0,
                                    'price': str(product.get_price_after_sale()),
                                    
                                    }

        if product.subtract == True:

            if product.stock <= self.cart[product_id]['quantity'] + quantity:
                quantity = product.stock     
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity

        else:
            self.cart[product_id]['quantity'] += quantity

        
        
        related = Product.objects.filter(related=True, parent=None)
        for rel in related:
            rel_id = str(rel.id)
            if rel_id not in self.cart:
                self.cart[rel_id] = {'quantity': rel.minimum,
                                     'free': rel.free,
                                    'price': str(rel.price),
                                    }
        
        cat = Category.objects.get(id=product.parent.id)
        cat_related = Product.objects.filter(related=True, parent=cat)

        for rel in cat_related:
            rel_id = str(rel.id)
            if rel_id not in self.cart:
                self.cart[rel_id] = {'quantity': rel.minimum,
                                     'free': rel.free,
                                    'price': str(rel.price),
                                    }
        self.save()


  

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def minus(self, product, quantity, update_quantity=False):
        self.session['active_balls'] = '0.00'
        product_id = str(product.id)
        
        if product.minimum < self.cart[product_id]['quantity']:
            self.cart[product_id]['quantity'] -= quantity
        

        if self.cart[product_id]['quantity'] == 0:
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

        self.save()


    def plus(self, product, quantity, update_quantity=False):
        self.session['active_balls'] = '0.00'
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
        self.session['active_balls'] = '0.00'
        """
        Удаление товара из корзины.
        """
        try:
            product_id = str(product.id)
        except:
            product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def add_constructor(self, id, quantity, radio, checkbox, price):
        self.session['active_balls'] = '0.00'

        products = radio.replace(' ', '').replace('[', '').replace(']', '') + ','+ checkbox.replace(' ', '').replace('[', '').replace(']', '')
        constructor = id + radio.replace(' ', '').replace(',', '').replace('[', '').replace(']', '') + checkbox.replace(' ', '').replace(',', '').replace('[', '').replace(']', '')
        
        if constructor not in self.constructors:

            self.constructors[constructor] = {
                'id': constructor,
                'constructor': int(id),
                'quantity': int(quantity),
                'price': str(price),
                'products': products
                }
            

        else:
            
            self.constructors[constructor]['quantity'] += int(quantity)
        
        self.session.modified = True
        self.save()

    def plus_constructor(self, constructor):

        self.constructors[constructor]['quantity'] += 1
        self.session.modified = True
        self.save()


    def minus_constructor(self, constructor):
        self.constructors[constructor]['quantity'] -= 1
        self.session.modified = True
        self.save()

    def remove_constructor(self, constructor):

        del self.constructors[constructor]
        self.session.modified = True
        self.save()

    def get_constructors(self):
        constructor_list = []
        for item in self.constructors.values():
            try:
                products = item['products'].split(',')
                constructor = FoodConstructor.objects.get(id=item['constructor'])
                constructor_items = []
                for i in products:
                    try:
                        item_c = Ingridients.objects.get(id=str(i))
                        constructor_items.append(item_c)
                    except: 
                        pass

                constructor_list.append({
                    'id': item['id'],
                    'constructor': constructor,
                    'price': Decimal(item['price']),
                    'quantity': item['quantity'],
                    'items': constructor_items
                })

            except:
                pass


        return constructor_list

    def constructor_clear(self):
        items = self.constructors.keys()
        for item in list(items):
            if item != 0:
                del self.constructors[item]
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

            free_item = (item['price'] * item['free'])
            if item['quantity'] < item['free']:
                free_item = (item['free'] - item['quantity']) * item['price']

            item['total_price'] = (item['price'] * item['quantity']) - free_item
            yield item

        


    def __len__(self):
       
        """
        Подсчет всех товаров в корзине.
        """
        all_len = sum(item['quantity'] for item in self.cart.values())
        

        return all_len + self.count_combos() + self.count_options() + self.count_constructors()


    def get_delivery(self):
        
        
        a = self.get_total_price()
        b = self.get_discount()
        d = ((self.get_personal_sale()/Decimal('100') * self.get_total_price()))
        e = self.active_balls 
        f = self.get_first_delivery_summ()
        g = self.get_discount_on_pickup()
        total_price = a - b - d - e - f - g

        
        res = self.get_delivery_sum
        
        if total_price == 0:
            
            res = Decimal(0)

        
        if not del_zones:
            if self.get_d != 1:
                res = Decimal(0)
            
            res = Decimal(self.get_delivery_sum) if total_price < Decimal(self.free_delivery) else Decimal(0)
            return res

        if self.get_d != 1:
            res = Decimal(0)
            return res

        if self.get_delivery_sum:
            
            if self.free_delivery != '0':
                res = Decimal(self.get_delivery_sum) if total_price < Decimal(self.free_delivery) else Decimal(0)
               
            elif self.free_delivery == '0':
                
                res = Decimal(self.get_delivery_sum)

            

        
        
        if delivery_integrations:
            
            # Если есть скидка на доставку в Delivery, то берем ее (Процент скидки на доставку (компенсация за доставку))
            sale_persent_get = delivery_integrations.sale_persent
            if sale_persent_get:
                sale_persent = delivery_integrations.sale_persent
            else:
                sale_persent = 0
           
            # Если есть скидка на доставку в Delivery, то берем ее (Сумма заказа, от которой начинает работать компенсация за доставку)
            summ_persent_get = delivery_integrations.summ_persent
            if summ_persent_get:
                summ_persent = delivery_integrations.summ_persent
            else:
                summ_persent = 0
           
            # Если есть скидка на доставку в Delivery, то берем ее (Сумма доставки, от которой начинает работать компенсация за доставку)
            delivery_summ_persent_get = delivery_integrations.delivery_summ_persent
            if delivery_summ_persent_get:
                delivery_summ_persent = delivery_integrations.delivery_summ_persent
            else:
                delivery_summ_persent = 0

            # Считаем процент скидки
            res_percent = math.ceil(res / 100 * sale_persent)
            

        
            if summ_persent != 0 and total_price >= summ_persent:
                res = res - res_percent

            if delivery_summ_persent != 0 and res >= delivery_summ_persent:
                res = res - res_percent
                
       

        
        return res
    

    # Добавляем адрес
    def add_address(self, delivery_address):

        self.delivery_address = delivery_address
        self.session.modified = True
        self.save()

    def add_phone(self, phone):

        self.phone = phone
        self.session.modified = True
        self.save()

    def return_phone(self):

        return self.phone

 


    def add_delivery_summ(self, delivery_summ, free_delivery):

        self.get_delivery_sum = delivery_summ
        self.free_delivery = free_delivery

        self.session.modified = True
        self.save()

    
    def add_min_delivery(self, min_delivery):

        self.min_delivery = min_delivery
        self.session.modified = True
        self.save()




    def get_min_delivery(self):

        return Decimal(self.min_delivery)
    

    def get_minimum_persent(self):

        min_delivery = self.get_min_delivery()
        price = self.get_total_price()

        persent = (Decimal(price) / Decimal(min_delivery)) * Decimal(100)


        return int(persent)
        


    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        res = Decimal('0')

        for item in self.cart.values():

            free_item = (Decimal(item['price']) * item['free'])
            if item['quantity'] < item['free']:
                free_item = (item['free'] - item['quantity']) * Decimal(item['price'])


            item_price = Decimal(item['price']) * item['quantity']

            res += item_price - free_item

        total_pr = Decimal(res)

        return total_pr + self.combo_summ() + self.options_summ() + self.constructors_summ()


    def clear(self):
        # удаление корзины из сессии
        self.session['coupon_id'] = None
        self.session.modified = True
        self.first_delivery = 0
        del self.first_delivery
        del self.session[settings.CART_SESSION_ID]
        

    
    def get_personal_sale(self):

        if LoyaltyCardSettings.objects.get().active == True:

            return self.percent_down
        
        else:

            return 0
    


    def get_personal_balls(self):

        

        result = Decimal(self.balls) - Decimal(self.active_balls)

        return result
        
        
    
    # Активируем баллы для списания
    def get_max_balls(self):
        
        a = self.get_total_price()
        # print(a)
        max_bonus = (Decimal(a) / Decimal('100')) * Decimal(self.percent_pay)

        if Decimal(max_bonus) >= Decimal(self.balls):
            max_bonus = self.balls


        return Decimal(max_bonus)

       
    def get_personal_pay(self):
        return self.percent_pay


    def get_total(self):

        return self.get_total_price() + self.get_delivery()

        

    def get_free(self):
        
        return self.free_delivery
    
    def add_first_delivery_persent(self, first_delivery):

        self.first_delivery = first_delivery
    
    def get_first_delivery_summ(self):

        summ = self.get_total_price() / 100 * self.first_delivery

        return summ

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')
    

    def get_discount_on_pickup(self):
        if self.get_d == 0:
            result = self.get_total_price() / 100 * ShopSetup.objects.get().discount_on_pickup
        else:
            result = 0

        return result

    def get_discount_on_pickup_persent(self):
        if self.get_d == 0:
            result = ShopSetup.objects.get().discount_on_pickup
        else:
            result = 0

        return result


    def get_total_price_after_discount(self):
        a = self.get_total_price()
        b = self.get_discount()
        c = self.get_delivery()
        d = ((self.get_personal_sale()/Decimal('100') * self.get_total_price()))
        e = self.active_balls 
        f = self.get_first_delivery_summ()
        g = self.get_discount_on_pickup()
        
        res = a - b + c - d - e - f - g
        return res