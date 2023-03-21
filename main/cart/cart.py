from decimal import Decimal
from django.conf import settings
from shop.models import Category, Combo, ComboItem, Product, Product, ShopSetup
from coupons.models import Coupon
from accounts.models import LoyaltyCardSettings, LoyaltyCard, UserProfile
import decimal
D = decimal.Decimal

try:
    del_zones = ShopSetup.objects.get().zones_delivery
except:
    del_zones = False


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



        # Программа лояльности
        try:
            user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
            loyalty_card = LoyaltyCard.objects.get(user=user_profile)
            

            percent_up = loyalty_card.status().percent_up
            percent_down = loyalty_card.status().percent_down
            percent_pay = loyalty_card.status().percent_pay
            balls = loyalty_card.balls
            

        except Exception as e:
            print(e)
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



        # сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')


        get_d = request.session.get('delivery')
        get_sum = request.session.get('delivery_summ')

        if not get_sum:
            self.get_d = 0
        self.get_sum = get_sum

        if not get_d:
            self.get_d = 1
        self.get_d = get_d


        
       
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


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




    def count_combos(self):
        combo_len = sum(int(item['quantity']) for item in self.combos.values())
        return combo_len
    


    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        self.session['active_balls'] = '0.00'

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'free': 0,
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

        
        
        related = Product.objects.filter(related=True)
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
            item['total_price'] = (item['price'] * item['quantity']) - (item['price'] * item['free'])
           

            yield item

        
        



    def __len__(self):
       
        """
        Подсчет всех товаров в корзине.
        """
        all_len = sum(item['quantity'] for item in self.cart.values())
        

        return all_len + self.count_combos()


    def get_delivery(self):
        if del_zones:
            if self.get_d == 1:
                if self.get_sum:
                    if Decimal(self.get_total_price()) >= Decimal(free_delivery):
                        summ = Decimal(0)
                        return summ
                    else:
                        return Decimal(self.get_sum)
                else:
                    summ = Decimal(0)
                    return summ
            else:
                summ = Decimal(0)
                return summ
        else:
            if self.get_d == 1:
                if Decimal(self.get_total_price()) >= Decimal(free_delivery):
                    summ = Decimal(0)
                    return summ
                else:
                    return Decimal(price_delivery)
            else:
                summ = Decimal(0)
                return summ

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        total_pr = sum((Decimal(item['price']) * item['quantity']) - (Decimal(item['price']) * item['free']) for item in self.cart.values())

        return total_pr + self.combo_summ()


    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session['coupon_id'] = None
        self.session.modified = True

    
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
        a = self.get_total_price()
        b = self.get_discount()
        c = self.get_delivery()
        d = ((self.get_personal_sale()/Decimal('100') * self.get_total_price()))
        e = self.active_balls 
        
        
        return a - b + c - d - e