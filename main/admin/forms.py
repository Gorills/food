from django import forms
from coupons.models import Coupon
from subdomains.models import Subdomain
from orders.models import Order 
from setup.models import BaseSettings, Colors, RecaptchaSettings, EmailSettings, ThemeSettings, CustomCode, Fonts
from shop.models import AutoFieldOptions, Category, Combo, Product, Manufacturer, OptionType, CharGroup, CharName, ProductChar, ProductOption, ProductImage, ProductSale, ShopSetup, PickupAreas, PayMethod, WorkDay, FoodConstructor, ConstructorCategory, Ingridients, DeliveryTimePrice
from blog.models import BlogCategory, BlogSetup, Post, PostBlock
from home.models import PlaceImages, SliderSetup, Slider, Page, Reviews
from accounts.models import LoyaltyCard, LoyaltyCardSettings, LoyaltyCardStatus
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from pay.models import PaymentSet, Tinkoff, Yookassa, AlfaBank, PayKeeper
from integrations.models import Integrations
from delivery.models import Delivery



class ReviewsForm(forms.ModelForm):
    text = forms.CharField(label='Текст', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = Reviews
        fields = [
            'name',
            'image',
            'text',
            'scores',
            'date',
            'link',
            'page',
            'platform',
            'view_home',
            'status'

        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'text': forms.Textarea(attrs={
                'class': 'input',
            }),
            'scores': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'date': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
            }),
            'link': forms.TextInput(attrs={
                'class': 'input',
            }),
            'page': forms.Select(attrs={
                'class': 'input',
            }),
            'platform': forms.Select(attrs={
                'class': 'input',
            }),
        }


class DeliveryTimePriceForm(forms.ModelForm):
    class Meta:
        model = DeliveryTimePrice
        fields = '__all__'

        widgets = {
           
            'start_delivery': forms.TimeInput(attrs={
                'class': 'input',
                'type': 'time',
            }),
            'end_delivery': forms.TimeInput(attrs={
                'class': 'input',
                'type': 'time',
            }),
            'price_delivery': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'free_delivery': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'min_delivery': forms.NumberInput(attrs={
                'class': 'input',
            }),
        }


class IngridientsForm(forms.ModelForm):
    class Meta:
        model = Ingridients
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'input',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'parent': forms.Select(attrs={
                'class': 'input',
            }),
            'not_ingridient': forms.SelectMultiple(attrs={
                'class': 'input',
            }),
            'extra_charge': forms.NumberInput(attrs={
                'class': 'input',
            }),
        }



class ConstructorCategoryForm(forms.ModelForm):
    class Meta:
        model = ConstructorCategory
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'parent': forms.Select(attrs={
                'class': 'input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'input',
            }),
            'category_class': forms.Select(attrs={
                'class': 'input',
                'required': 'required'
            }),
            'minimum': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'maximum': forms.NumberInput(attrs={
                'class': 'input',
            })
        }



class FoodConstructorForm(forms.ModelForm):
    class Meta:
        model = FoodConstructor
        fields = '__all__'

        widgets = {
            
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'input',
            }),
            'weight': forms.TextInput(attrs={
                'class': 'input',
            }),
            'btn_text': forms.TextInput(attrs={
                'class': 'input',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'parent': forms.Select(attrs={
                'class': 'input',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
            }),
        }



class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'

        widgets = {
            'name': forms.Select(attrs={
                'class': 'input',
            }),
            'api_key': forms.TextInput(attrs={
                'class': 'input',
            }),

        }




class WorksdayForm(forms.ModelForm):
    class Meta:
        model = WorkDay
        fields = '__all__'

        widgets = {
            'day': forms.Select(attrs={
                'class': 'input',
            }),
            'start_delivery': forms.TextInput(attrs={
                'class': 'input',
                'type': 'time'
            }),
            'end_delivery': forms.TextInput(attrs={
                'class': 'input',
                 'type': 'time'
            }),

        }


class IntegrationsForm(forms.ModelForm):
    class Meta:
        model = Integrations
        fields = '__all__'

        widgets = {
            'name': forms.Select(attrs={
                'class': 'input',
            }),
            'api_key': forms.TextInput(attrs={
                'class': 'input',
            }),
            'webhook_uri': forms.TextInput(attrs={
                'class': 'input',
            }),
            'webhook_token': forms.TextInput(attrs={
                'class': 'input',
            })

        }

        

class FontForm(forms.ModelForm):
    class Meta:
        model = Fonts
        fields = '__all__'

        widgets = {
            'name': forms.Select(attrs={
                'class': 'input',
            }),
        }
        labels = {
            'name': 'Шрифт',
        }



class CustomCodeForm(forms.ModelForm):
    class Meta:
        model = CustomCode
        fields = '__all__'

        widgets = { 
            'code' : forms.Textarea(attrs={
                'class': 'input',
            }),
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'subdomain': forms.Select(attrs={
                'class': 'input',
            }),
        }





class SubdomainsForm(forms.ModelForm):
    text = forms.CharField(label='Текст', required=False, widget=CKEditorUploadingWidget())
   
    class Meta:
        model = Subdomain
        fields = [
            'name',
            'subdomain',
            
            'telegram_group',

            'phone',
            'email',
            'telegram',
            'city',
            'address',
            'vk',
            'whatsapp',
            'viber',
            'ok',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'meta_h1',
            'text',
            
            
        ]
        widgets = {
           'name': forms.TextInput(attrs={
               'class': 'input',
           }),
           'subdomain': forms.TextInput(attrs={
               'class': 'input',
           }),
           'phone': forms.TextInput(attrs={
               'class': 'input',
           }),
           'email': forms.TextInput(attrs={
               'class': 'input',
           }),
           'telegram_bot': forms.TextInput(attrs={
               'class': 'input',
           }),
           'city': forms.TextInput(attrs={
               'class': 'input',
           }),
           'address': forms.TextInput(attrs={
               'class': 'input',
           }),
           'vk': forms.TextInput(attrs={
               'class': 'input',
           }),
           'whatsapp': forms.TextInput(attrs={
               'class': 'input',
           }),
           'telegram': forms.TextInput(attrs={
               'class': 'input',
           }),
           'telegram_group': forms.TextInput(attrs={
               'class': 'input',
           }),
           'viber': forms.TextInput(attrs={
               'class': 'input',
           }),
           'ok': forms.TextInput(attrs={
               'class': 'input',
           }),
           'meta_title': forms.TextInput(attrs={
               'class': 'input',
           }),
           'meta_description': forms.Textarea(attrs={
               'class': 'input',
           }),
           'meta_keywords': forms.TextInput(attrs={
               'class': 'input',
           }),
           'meta_h1': forms.TextInput(attrs={
               'class': 'input',
           })
           
            
        }






class AutoFieldOptionsForm(forms.ModelForm):
    class Meta:
        model = AutoFieldOptions
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'value' : forms.TextInput(attrs={
                'class': 'input',
            }),
            'price' : forms.TextInput(attrs={
                'class': 'input',
            }),
            'weight' : forms.TextInput(attrs={
                'class': 'input',
            }),
            'parent': forms.Select(attrs={
                'class': 'input',
            })
        }




# Комбо


class ComboForm(forms.ModelForm):
    class Meta:
        model = Combo
        fields = '__all__'
        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'price': forms.TextInput(attrs={
                'class': 'input',
                'type': 'number'
            }),
           
        }



# Карты лояльности

class LoyaltyCardForm(forms.ModelForm):
    class Meta:
        model = LoyaltyCard
        fields = '__all__'
        widgets = {
           
            'user': forms.Select(attrs={
                'class': 'input',
            }),
            'code': forms.TextInput(attrs={
                'class': 'input',
            }),
            'summ': forms.TextInput(attrs={
                'class': 'input',
            }),
            'balls': forms.TextInput(attrs={
                'class': 'input',
            }),
         
        }



# Статусы карт лояльности
class LoyaltyCardStatusForm(forms.ModelForm):
    class Meta:
        model = LoyaltyCardStatus
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'summ': forms.TextInput(attrs={
                'class': 'input',
            }),
            'percent_up': forms.TextInput(attrs={
                'class': 'input',
            }),
            'percent_down': forms.TextInput(attrs={
                'class': 'input',
            }),
            'percent_pay': forms.TextInput(attrs={
                'class': 'input',
            }),
        }



# Настройка карт лояльности

class LoyaltyCardSettingsForm(forms.ModelForm):
    text = forms.CharField(label='Описание программы лояльности', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = LoyaltyCardSettings
        fields = '__all__'
        




# Сопутствующие товары
class RelatedProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'related',
            'name',
            'price',
            'free',
            'all_cats',
            'minimum',
            'parent',
            'thumb'
        ]

        widgets = {
            'related': forms.CheckboxInput(attrs={
                'hidden': 'hidden'
            }),
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'price': forms.TextInput(attrs={
                'class': 'input',
            }),
            'free': forms.TextInput(attrs={
                'class': 'input',
            }),
            'minimum': forms.TextInput(attrs={
                'class': 'input',
            }),
            'parent': forms.Select(attrs={
                'class': 'input',
            }),

        }

        labels = {
            'parent': 'Категория (не обязательно)',
            'name': 'Название',
            'related': ''
          
        }


# Способы оплаты
class PayMethodForm(forms.ModelForm):
    class Meta:
        model = PayMethod
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
            })

        }





# Зоны самовывоза

class PickupAreasForm(forms.ModelForm):
    class Meta:
        model = PickupAreas
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'address': forms.TextInput(attrs={
                'class': 'input',
            }),
            'time_to_open': forms.TextInput(attrs={
                'class': 'input',
                
            }),
            'time_to_close': forms.TextInput(attrs={
                'class': 'input',
                
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input',
            }),
            'dop_info': forms.TextInput(attrs={
                'class': 'input',
            }),
            'city': forms.Select(attrs={
                'class': 'input',
            }),
        }





# Платежи


class YookassaForm(forms.ModelForm):
    class Meta:
        model = Yookassa
        fields = '__all__'
        
        widgets = {
            'shop_id': forms.TextInput(attrs={
                'class': 'input',
            }),
            'key': forms.TextInput(attrs={
                'class': 'input',
            }),
            
           
            'vat_code': forms.Select(attrs={
                'class': 'input',
            }),
        }

class AlfaBankForm(forms.ModelForm):
    class Meta:
        model = AlfaBank
        fields = '__all__'
        
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'input',
            }),
            'password': forms.TextInput(attrs={
                'class': 'input',
            }),
            'token': forms.TextInput(attrs={
                'class': 'input',
            })
        }



class PayKeeperForm(forms.ModelForm):
    class Meta:
        model = PayKeeper
        fields = '__all__'
        
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'input',
            }),
            'password': forms.TextInput(attrs={
                'class': 'input',
            }),
            'server': forms.TextInput(attrs={
                'class': 'input',
            })
        }


class TinkoffForm(forms.ModelForm):
    class Meta:
        model = Tinkoff
        fields = '__all__'
        
        widgets = {
            'terminalkey': forms.TextInput(attrs={
                'class': 'input',
            }),
            'password': forms.TextInput(attrs={
                'class': 'input',
            }),
            'taxation': forms.Select(attrs={
                'class': 'input',
            })
        }



class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentSet
        fields = '__all__'
        
        widgets = {
           
            'name': forms.Select(attrs={
                'class': 'input',
            }),
        }






# Статус заказа
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'status'
        ]
        widgets = {
           
            'status': forms.Select(attrs={
                'class': 'input',
            }),
        }




# Изображения зала

class ImageForm(forms.ModelForm):
    class Meta:
        model = PlaceImages
        fields = '__all__'
        
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'input',
            }),
        }


# Страницы 
class PageForm(forms.ModelForm):
    text = forms.CharField(label='Текст страницы', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = Page
        fields = "__all__"
        
        widgets = {
           
            'type': forms.Select(attrs={
                'class': 'input',
            }),
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
            }),
           
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
            }),
        }



# Cлайдер

class SliderSetupForm(forms.ModelForm):
    
    class Meta:
        model = SliderSetup
        fields = "__all__"
        widgets = {
            'speed': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            })
        }



class SliderForm(forms.ModelForm):
    
    class Meta:
        model = Slider
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название',
            }),
            'title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок (не обязательно)',
            }),
            'text': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Текст (не обязательно)',
            }),
            'button_text': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Текст кнопки (не обязательно)',
            }),
            'link': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ссылка (не обязательно)',
            }),
            'day': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Ссылка (не обязательно)',
            }),
        }



# Блог

class BlogSetupForm(forms.ModelForm):
    description = forms.CharField(label='Описание блога', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = BlogSetup
        fields = "__all__"
        widgets = {
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
        }


class PostBlockForm(forms.ModelForm):
    # text = forms.CharField(label='Текст', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = PostBlock
        fields = [
            'parent',
            'type',
            'text',
            'title',
            'image',
            'video',
            'order',

        ]
        labels = {
            'title': 'Заголовок',
          
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input submit',
                'placeholder': 'Заголовок',
            }),
            'text': forms.Textarea(attrs={
                'class': 'input submit',
                'placeholder': 'Текст',
            }),
            'video': forms.FileInput(attrs={
                'class': 'submit-file',
                'accept': 'video/*'
            
            }),
            'image': forms.FileInput(attrs={
                'class': 'submit-file',
                'accept': 'image/*'
                
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'parent',
            'name',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'slug',
        ]   
        labels = {
            'parent': 'Категория',
            'name': 'Название',
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета тайтл',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'image': 'Изображение',
            'slug': 'SEO URL',
        }
        widgets = {
            'parent': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Категория',
                'required': 'required'
            }),
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета тайтл',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
            'image': forms.FileInput(attrs={
                
                'required': 'required'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
        }

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory

        fields = [
            'name',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'slug',

        ]        
        labels = {
            'name': 'Название',
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета тайтл',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'image': 'Изображение',
            'slug': 'SEO URL',
        }
        widgets = {
          
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета тайтл',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
        }


# Настройка скидок на категории и товары
        
class ProductSaleForm(forms.ModelForm):
    class Meta:
        model = ProductSale
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': '',
            }),
            'date_start': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
            }),
            'date_end': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
            }),
            'time_start': forms.TimeInput(attrs={
                'class': 'input',
                'type': 'time',
            }),
            'time_end': forms.TimeInput(attrs={
                'class': 'input',
                'type': 'time',
            }),
            'percent': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': '',
            }),
            'categorys': forms.SelectMultiple(attrs={
                'class': 'input',
            }),
            'products': forms.SelectMultiple(attrs={
                'class': 'input',
            }),
        }



# Настройки магазина

class ShopSetupForm(forms.ModelForm):
    description = forms.CharField(label='Описание каталога', required=False, widget=CKEditorUploadingWidget())
    delivery_blocked_text = forms.CharField(label='Текст блокировки', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = ShopSetup
        fields = "__all__"
        widgets = {
            'status': forms.Select(attrs={
                'class': 'input',
                'placeholder': '',
            }),
            'work_time': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
                
            }),
             'start_delivery': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
                'type': 'time',
                'step': "1"
                
            }),
            
            'end_delivery': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
                'type': 'time',
                'step': "1"
                
            }),
            'interval': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
                'min': "30",
                'max': "60",
                'step': "30",
                'onkeypress': 'return false'
            }),
            'delay': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'price_delivery': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'free_delivery': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'min_delivery': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'first_delivery': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Скидка на 1 заказ в %',
            }),
            'discount_on_pickup': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Скидка при самовывозе',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'start_bonus': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'min_width': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'min_height': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'max_width': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'max_height': forms.NumberInput(attrs={
                'class': 'input',
            })
            
        }


# Маркетинг
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
        labels = {
            'code': 'Код купона',
            'valid_from': 'Дата начала акции',
            'valid_to': 'Дата окончания акции',
            'discount': 'Скидка',
            'active': 'Активность',
        }
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Код купона',
            }),
            'valid_from': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
                
            }),
            'valid_to': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
                
            }),

            
            'discount': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Скидка',
            }),
           
            
        }


# Товар и опции товара
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage

        fields = [
            'parent',
            'src'
        ]
        labels = {
            'src': 'Выбрать изображение'
        }
        

class ProductOptionForm(forms.ModelForm):
    class Meta:
        model = ProductOption
        fields = [
            'type',
            'parent',
            'option_sku',
            'option_value',
            'option_stock',
            'option_price',
            'option_subtract',
            'image_status',
            
        ]
        labels = {
            'type': 'Тип опции',
            # 'parent': 'Продукт',
            'option_sku': 'Артикул',
            'option_value': 'Значение',
            'option_stock': 'Количество',
            'option_price': 'Добавить стоимость',
            'option_subtract': 'Вычитать со склада',
            'image_status': 'Включить изображения',
           
        }
        widgets = {
            'type': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Тип опции',
            }),
            'option_value': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'option_sku': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Артикул',
            }),
            'option_stock': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Количество',
            }),
            'option_price': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Добавить стоимость',
            }),
            # 'option_subtract': forms.CheckboxInput(attrs={
            #     'class': 'input',
                
            # }),
        }


class ProductCharForm(forms.ModelForm):
    class Meta:
        model = ProductChar
        fields = [
            'char_name',
            
            'char_value',
        ]
        labels = {
            'char_name': 'Название характеристики',
            
            'char_value': 'Значение',
        }
        widgets = {
            'char_name': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Название характеристики',
                'id': 'id_char_name',
               
            }),
            'char_value': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
                'id': 'id_char_value'
            }),
        }

class CharGroupForm(forms.ModelForm):
    class Meta:
        model = CharGroup
        fields = [
            'name',
            
        ]
        labels = {
            'name': 'Название группы характеристик',
           
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название группы характеристик',
            }),
        }


class CharNameForm(forms.ModelForm):
    class Meta:
        model = CharName
        fields = [
            'group',
            'text_name',
            
        ]
        labels = {
            'group': 'Группа опций',
            'text_name': 'Название опции',
           
        }
        widgets = {
            'group': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Группа опций',
            }),
            'text_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название опции',
                'id': 'char_name'
            }),
        }


class OptionTypeForm(forms.ModelForm):
    class Meta:
        model = OptionType
        fields = [
            'name',
            'option_class',   
        ]
        labels = {
            'name': 'Название опции',
            'option_class': 'Тип опции',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название опции',
            }),
            'option_class': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Тип опции',
            }),
        
        }



class ManufacturerForm(forms.ModelForm):
    description = forms.CharField(label='Описание производителя', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = Manufacturer
        fields = [
            'name',
            'description',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'slug',
            'image',
            'sort_order',
        ]
        labels = {
            'name': 'Название производителя',
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета заголовок',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'slug': 'SEO URL',
            'image': 'Изображение',
            'sort_order': 'Порядок сортировки',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название производителя',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Порядок сортировки',
            }),
        }


class ProductForm(forms.ModelForm):
    
    description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Product
        fields = [
            'name',
            'short_description',
            'description',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'tags',
            
            'sku',
            'price',
            'old_price',
            'stock',
            'minimum',
            'subtract',
            'shipping',
            'new',
            'bestseller',
            'slug',
            
            'length',
            'width',
            'height',
            # 'color',
            # 'color_name',
            'length_class',
            'weight',
            'weight_class',
            'product_manufacturer',
            'parent',
            'product_connect',
            'thumb',
            'status',
            'sort_order',
        ]
        labels = {
            'name': 'Название товара',
            'short_description': 'Короткое описание товара',
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета заголовок',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'tags': 'Теги',
            'model': 'Модель',
            'sku': 'Артикул',
            'price': 'Цена (с учетом скидки)',
            'old_price': 'Старая цена',
            'stock': 'Количество',
            'minimum': 'Минимальное количество',
            'subtract': 'Вычитать со склада',
            'shipping': 'Необходима доставка',
            'new': 'Новинка',
            'bestseller': 'Хит продаж',
            'slug': 'SEO URL',
            
            'length': 'Длина',
            'width': 'Ширина',
            'height': 'Высота',
            # 'color': 'Цвет',
            # 'color_name': 'Название цвета',
            'length_class': 'Единица измерения длины',
            'weight': 'Вес',
            'weight_class': 'Единица измерения веса',
            'product_manufacturer': 'Производитель',
            'parent': 'Категория',
            'product_connect': 'Связанные товары',
            'thumb': 'Изображение товара (превью)',
            'status': 'Статус',
            'sort_order': 'Порядок сортировки',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название товара',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Короткое описание товара',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Теги',
            }),
            'model': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Модель',
            }),
            'sku': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Артикул',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Цена (с учетом скидки)',
            }),
            'old_price': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Старая цена',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Количество',
            }),
            'minimum': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Минимальное количество для заказа',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
            

            'length': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Длина',
            }),
            'width': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ширина',
            }),
            'height': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Высота',
            }),
            # 'color': forms.TextInput(attrs={
                
            #     'placeholder': 'Цвет',
            #     'type':'color',
            #     'required': 'required',
            # }),
            # 'color_name': forms.TextInput(attrs={
            #     'class': 'input',
            #     'placeholder': 'Название цвета',
            #     'required': 'required',
            # }),
            'length_class': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Единица измерения длины',
            }),
            'weight': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Вес',
            }),
            'weight_class': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Единица измерения веса',
            }),
            'product_manufacturer': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Производитель',
            }),
            'parent': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Категория',
            }),
            'product_connect': forms.SelectMultiple(attrs={
                'class': 'input',
                'placeholder': 'Связанные товары',
            }),
            
          
            # 'status': forms.Select(attrs={
            #     'class': 'input',
            #     'placeholder': 'Статус',
            # }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Порядок сортировки',
            }),
        }


class CategoryForm(forms.ModelForm):
    description = forms.CharField(label='Описание категории', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Category
        fields = [
            'parent',
            'name',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'top',
            'home',
            'resize',
            'font_color',
            'bg_color',
            'opacity',
            'sort_order',
            'status',
            'slug',
        ]
        labels = {
            

            'parent': 'Родительская категория',
            'name': 'Название категории',
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета заголовок',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            
            'image': 'Изображение категории',
            'top': 'Отображать в меню',
            'column': 'Количество колонок',
            'sort_order': 'Порядок сортировки',
            'status': 'Активная',
            'slug': 'SEO URL',
            
            
        }
        widgets = {
            'parent': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Родительская категория',
            }),
           
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название категории',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
           
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
          
            'font_color': forms.TextInput(attrs={
                # 'class': 'input',
                'type': 'color',
            }),
            'bg_color': forms.TextInput(attrs={
                # 'class': 'input',
                'type': 'color',
            }),
            'opacity': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Прозрачность изображения',
            }),
            'column': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Количество колонок',
            }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Порядок сортировки',
            }),
            'status': forms.CheckboxInput(attrs={
                'class': '',
                'placeholder': 'Активная',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
        }



class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = ThemeSettings
        fields = [
            'name'
        ]
        widgets = {
            'name': forms.Select(attrs={
                'placeholder': 'Тема',
                'class': 'input'
            }),
        }
        labels = {
            'name': 'Выбрать тему',
        
        }

class ColorsForm(forms.ModelForm):
    class Meta:
        model = Colors
        fields = [
            'primary',
            'secondary',
            'success',
            'danger',
            'warning',
            'info',
            'header_bg',
            'header_font',
            'footer_color',
            'footer_font',
            'body_bg',
            'body_font',
            
            'search_bg',
            'search_font',
            'mobile_menu_bg',
            'mobile_menu_font',

            'product_card_bg',
            'product_card_font',
            'gray',

            'bg_btn',
            'border_btn',
            'color_btn',
            'color_btn_light',
            'cart_border',
            'cart_fonts_color',
            'cart_bg',
            'bg_image',
            'header_image',
            'footer_image',
            'product_detail_image'
        ]
        widgets = {
            'cart_fonts_color': forms.TextInput(attrs={
                'type': 'color'
            }),
            'cart_border': forms.TextInput(attrs={
                'type': 'color'
            }),
            'cart_bg': forms.TextInput(attrs={
                'type': 'color'
            }),

            'search_bg': forms.TextInput(attrs={
                'type': 'color'
            }),
            'search_font': forms.TextInput(attrs={
                'type': 'color'
            }),
            'mobile_menu_bg': forms.TextInput(attrs={
                'type': 'color'
            }),
            'mobile_menu_font': forms.TextInput(attrs={
                'type': 'color'
            }),

            'primary': forms.TextInput(attrs={
                
                'placeholder': 'Основной цвет',
                'type': 'color'
            }),
            'secondary': forms.TextInput(attrs={
                
                'placeholder': 'Дополнительный цвет',
                'type': 'color'
            }),
            'success': forms.TextInput(attrs={
                
                'placeholder': 'Цвет успеха',
                'type': 'color'
            }),
            'danger': forms.TextInput(attrs={
                
                'placeholder': 'Цвет ошибки',
                'type': 'color'
            }),
            'warning': forms.TextInput(attrs={
                
                'placeholder': 'Цвет предупреждения',
                'type': 'color'
            }),
            'info': forms.TextInput(attrs={
                
                'placeholder': 'Цвет инфо',
                'type': 'color'
            }),
            'header_bg': forms.TextInput(attrs={
                
                'placeholder': 'Цвет header',
                'type': 'color'
            }),
            'header_font': forms.TextInput(attrs={
                
                'placeholder': 'Цвет шрифтов в header',
                'type': 'color'
            }),
            'footer_color': forms.TextInput(attrs={

                'placeholder': 'Цвет footer',
                'type': 'color'
            }),
            'footer_font': forms.TextInput(attrs={
                 'type': 'color'
            }),
            'body_bg': forms.TextInput(attrs={
                
                'placeholder': 'Цвет фона сайта',
                'type': 'color'
            }),
            'body_font': forms.TextInput(attrs={
                
                'placeholder': 'Цвет шрифтов сайта',
                'type': 'color'
            }),
            'gray': forms.TextInput(attrs={
                'placeholder': 'Цвет каталогов',
                'type': 'color'
            }),
            'bg_btn': forms.TextInput(attrs={
                
                'placeholder': 'Цвет кнопок',
                'type': 'color'
            }),
            'border_btn': forms.TextInput(attrs={
                
                'placeholder': 'Цвет обводки кнопок',
                'type': 'color'
            }),
            'color_btn': forms.TextInput(attrs={
                
                'placeholder': 'Цвет шрифтов в кнопках',
                'type': 'color'
            }),
            'color_btn_light': forms.TextInput(attrs={
                
                'placeholder': 'Цвет шрифтов в кнопках без фона',
                'type': 'color'
            }),
            'product_card_bg': forms.TextInput(attrs={
                'type': 'color'
            }),
            'product_card_font': forms.TextInput(attrs={
                'type': 'color'

            }),
            
        }
        labels = {
            'search_bg': 'Цвет поиска',
            'search_font': 'Цвет шрифтов в поиске',
            'mobile_menu_bg': 'Цвет мобильного меню',
            'mobile_menu_font': 'Цвет шрифтов в мобильном меню',
            'primary': 'Основной цвет',
            'secondary': 'Дополнительный цвет',
            'success': 'Цвет успеха',
            'danger': 'Цвет ошибки',
            'warning': 'Цвет предупреждения',
            'info': 'Цвет инфо',
            'header_bg': 'Цвет header',
            'header_font': 'Цвет шрифтов в header',
            'product_card_bg': 'Цвет карточки товара',
            'product_card_font': 'Цвет шрифтов в карточке',
            'catalog_bg': 'Цвет каталога',
            'cart_bg': 'Цвет фона корзины',
            'body_bg': 'Цвет фона сайта',
            'body_font': 'Цвет шрифтов сайта',
            'gray': 'Цвет каталогов',
            'bg_btn': 'Цвет кнопок',
            'border_btn': 'Цвет обводки кнопок',
            'color_btn': 'Цвет шрифтов в кнопках',
            'color_btn_light': 'Цвет шрифтов в кнопках без фона',
        }

class RecaptchaSettingsForm(forms.ModelForm):
    class Meta:
        model = RecaptchaSettings
        fields = [
            'recaptcha_private_key',
            'recaptcha_public_key',
            'recaptcha_default_action',
            'recaptcha_score_threshold',
            'recaptcha_language',
        ]

        widgets = {
            'recaptcha_private_key': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_private_key',
            }),
            'recaptcha_public_key': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_public_key',
            }),
            'recaptcha_default_action': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_default_action',
            }),
            'recaptcha_score_threshold': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_score_threshold',
            }),
            'recaptcha_language': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_language',
            }),
        }
      

class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = [
            'host',
            'host_user',
            'host_password',
            'host_from',
            'host_port',
            'use_ssl',
            'use_tls',

        ]

        widgets = {
            'host': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host',
            }),
            'host_user': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host_user',
            }),
            'host_password': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host_password',
            }),
            'host_from': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host_from',
            }),
            'host_port': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host_port',
            }),
        }
      



class SetupForm(forms.ModelForm):
    text = forms.CharField(label='Текст на главной странице', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = BaseSettings
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название сайта',
                
            }),
            'vk': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ссылка на VK',
                
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ссылка на WhatsApp',
                
            }),
            'telegram': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ссылка на Telegram',
                
            }),
            'viber': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ссылка на Viber',
                
            }),
            'ok': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ссылка на OK',
                
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Телефон',
                
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Email для клиентов'
            }),
            'telegram_bot': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Телеграм бот TOKEN'
            }),
            'telegram_group': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Группа в телеграме'
            }),
            'email_for_order': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Email для заявок'
            }),
            'copy_year': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Год копирайта',
                
            }),
            'city': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Город',
                
            }),
            'copy': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Копирайт',
                
            }),
            'address': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Адрес',
                
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок H1',
                
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
                
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
                
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
                
            }),
            'time_zone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
                
            }),
            'theme_color': forms.TextInput(attrs={
                
                'placeholder': 'Основной цвет',
                'type': 'color'
                
            }),
           'sms_pilot_apikey': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
                
            }),
            'sms_text': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Текст сообщения. Например: Поступил заказ на сумму {summ}. Номер заказа {order}',
                
            }),
            'logo_height': forms.TextInput(attrs={
                'class': 'input',
            }),
            'logo_width': forms.TextInput(attrs={
                'class': 'input',
            }),
           
           
        }
        labels = {
            'name': 'Название сайта',
            'phone': 'Телефон',
            'email': 'Email для клиентов',
            'email_for_order': 'Email для заявок',
            'telegram_bot': 'Телеграм бот TOKEN',
            'telegram_group': 'Группа в телеграм',
            'sms_pilot_apikey': 'API ключ от smspilot.ru',
            'sms_text': 'Текст сообщения при оформлении заказа (Зарегистрируйте шаблон на сайте https://smspilot.ru/. Сообщение будет отправляться только после регистрации шаблона. В тексте сообщения используйте {order}, для указания номера заказа, {summ} для указания суммы)',
            'copy_year': 'Год копирайта',
            'copy': 'Копирайт',
            'city': 'Город',
            'address': 'Адрес',
            'time_zone': 'Часовой пояс',

            
            'meta_h1': 'Заголовок H1',
            'meta_title': 'Мета заголовок',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'social_image': 'Изображение для соц.сетей',
            'logo_dark': 'Логотип в шапке',
            'logo_height': 'Высота логотипа (по умолчанию 60px)',
            'logo_width': 'Ширина логотипа',
            'logo_light': 'Логотип в подвале',
            
            'icon_ico': 'Иконка .ico',
            'icon_png': 'Иконка .png',
            'icon_svg': 'Иконка .svg',
            'pay_image': 'Изображение банков',
            'theme_color': 'Основной цвет',
            
            'active': 'Разрешить индексацию',
            'sms': 'Разрешить отправку смс сообщений для регистрации и подтверждения заказов',
            'debugging_mode': 'Режим разработки (вывод текстовой информации об ошибках)',
           
        }