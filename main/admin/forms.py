from django import forms
from coupons.models import Coupon
from subdomains.models import Subdomain
from orders.models import Order, OrderStatus 
from setup.models import BaseSettings, Colors, RecaptchaSettings, EmailSettings, ThemeSettings, CustomCode, Fonts, SoundSettings
from shop.models import AutoFieldOptions, Category, Combo, Product, Manufacturer, OptionType, CharGroup, CharName, ProductChar, ProductOption, ProductImage, ProductSale, ShopSetup, DopItems, PickupAreas, PayMethod, WorkDay, FoodConstructor, ConstructorCategory, Ingridients, DeliveryTimePrice
from blog.models import BlogCategory, BlogSetup, Post, PostBlock
from home.models import PlaceImages, SliderSetup, Slider, Page, Reviews, PageItem
from accounts.models import LoyaltyCard, LoyaltyCardSettings, LoyaltyCardStatus, UserRigts
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from pay.models import PaymentSet, Tinkoff, Yookassa, AlfaBank, PayKeeper
from integrations.models import Integrations
from delivery.models import Delivery
from django.contrib.auth.models import User




class SoundSettingsForm(forms.ModelForm):
    class Meta:
        model = SoundSettings
        fields = '__all__'

        widgets = {
            'sound': forms.Select(attrs={
                'class': 'input',
            })
        }


class UserRightsForm(forms.ModelForm):
    class Meta:
        model = UserRigts
        fields = '__all__'

        widgets = {
            'user': forms.TextInput(attrs={
                'hidden': 'hidden',
            }),

        }
        labels = {
            
            'user': '',
            
          
        }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'is_staff',
            'is_superuser',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'username': forms.TextInput(attrs={
                'class': 'input',
            }),
            'password': forms.PasswordInput(attrs={

                'class': 'input',
            }),
            'email': forms.TextInput(attrs={
                'class': 'input',
            })


        }



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
        fields = [
            'name',
            'summ',
            'percent_up',
            'percent_pay',
            'percent_pay_pickup',
        ]
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
          
            'percent_pay': forms.TextInput(attrs={
                'class': 'input',
            }),
            'percent_pay_pickup': forms.TextInput(attrs={
                'class': 'input',
            }),
        }



# Настройка карт лояльности

class LoyaltyCardSettingsForm(forms.ModelForm):
    # text = forms.CharField(label='Описание программы лояльности', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = LoyaltyCardSettings
        fields = [
            'active',
            'status_up',
            'status_down',
            'show_status',
            'show_summ',
            'balls_min_summ',
            'exclude_combos',
            'exclude_sales',
            'remove_sale_price',
            'enable_add_balls_after_first_order',
            'balls_after_first_order',
            'first_order_summ_for_add_balls',
        ]
        

        widgets = {
             'balls_min_summ': forms.TextInput(attrs={
                'class': 'input',
            }),
            'sms_text': forms.TextInput(attrs={
                'class': 'input',
            }),
            'balls_after_first_order': forms.TextInput(attrs={
                'class': 'input',
            }),
            'first_order_summ_for_add_balls': forms.TextInput(attrs={
                'class': 'input',
            })
            
        }


# Сопутствующие товары
class RelatedProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'related',
            'name',
            'price',
            'free',
            
            
            
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
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Получаем экземпляр заказа из формы (если уже существует)
        instance = kwargs.get('instance')
        if instance:
            delivery_method = instance.delivery_method
            # Получаем список статусов в зависимости от метода доставки
            status_choices = instance.get_status_class_choices()
            # Обновляем виджет поля status, чтобы отобразить соответствующие статусы
            self.fields['status'].widget.choices = status_choices
        else:
            # Если экземпляр еще не создан, обычно используются стандартные статусы
            self.fields['status'].widget.choices = Order.STATUS_CLASS



class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = OrderStatus
        fields = '__all__'



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


class PageItemForm(forms.ModelForm):
    text = forms.CharField(label='Текст блока', required=False, widget=CKEditorUploadingWidget())

    class Meta:
        model = PageItem
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'item_type': forms.Select(attrs={
                'class': 'input',
            }),
            'page': forms.Select(attrs={
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
            }),
            'height': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'height_mob': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'title_size': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'desc_size': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'image_compression': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'title_size': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'desc_size': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'title_size_mob': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'desc_size_mob': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'text_max_width': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
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
            'text_color': forms.TextInput(attrs={
               
                'placeholder': 'Цвет текста (не обязательно)',
                'type': 'color'
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
            'image_opacity': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'bg': forms.TextInput(attrs={
                
                'placeholder': 'Значение',  
                "type": "color"
            }),
            'order': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
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


class DopItemsForm(forms.ModelForm):
    class Meta:
        model = DopItems
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название',
            }),
            'description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input',
            })
        }



# Маркетинг
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'code',
            'valid_from',
            'valid_to',
            'discount',
            'active',
            'promo_type',
        ]
        labels = {
            'code': 'Код купона',
            'valid_from': 'Дата начала акции',
            'valid_to': 'Дата окончания акции',
            'discount': 'Скидка',
            'active': 'Активность',
            'promo_type': 'Действие промокода',
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

            'promo_type': forms.Select(attrs={
                'class': 'input',
                
            })
           
            
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
            'active', 
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


def get_unique_slug(slug):
    # Функция, чтобы обеспечить уникальность slug
    # Возможно, вам потребуется настроить его для вашей модели
    # Например, добавить случайные символы к slug, если он уже существует
    unique_slug = slug
    counter = 1
    while Product.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug

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
            'protein',
            'fat',
            'carb',
            'nutritional_value',
            'product_manufacturer',
            'parent',
            'product_connect',
            'parent_add',
            'thumb',
            'status',
            'sort_order',
            'in_cart',
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
            'protein': 'Белки',
            'fat': 'Жиры',
            'carb': 'Углеводы',
            'nutritional_value': 'Энергетическая ценность',

            'product_manufacturer': 'Производитель',
            'parent': 'Категория',
            'parent_add': 'Добавить категорию',
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
            'protein': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Белки',
            }),
            'fat': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Жиры',
            }),
            'carb': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Углеводы',
            }),
            'nutritional_value': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Энергетическая ценность',
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
            
            'parent_add': forms.SelectMultiple(attrs={
                'class': 'input',
                'placeholder': 'Свзянные категории',
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

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if self.instance.pk is None:  # Проверяем, является ли объект новым (не сохраненным в базу данных)
            try:
                Product.objects.get(slug=slug)
                new_slug = get_unique_slug(slug)
                return new_slug
            except Product.DoesNotExist:
                return slug
        else:
            return slug
        
        
class CategoryForm(forms.ModelForm):
    description = forms.CharField(label='Описание категории', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Category
        fields = [
            'parent',
            'name',
            'short_description',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'top',
            'home',
            'exclude_actions',
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
            'short_description': 'Короткое описание категории',
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
            'exclude_actions': 'Исключить из скидок и бонусов',
            
            
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
            'font_size',
            'header_bg',
            'header_font',
            'phone_color',
            'phone_decorations',
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
            'phone_color': forms.TextInput(attrs={
                'type': 'color'
            }),
            'font_size': forms.TextInput(attrs={
                'type': 'text',
                'class': 'input',
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
      



from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

class ImagePreviewWidget(ClearableFileInput):
    """
    Виджет для предпросмотра изображения с возможностью загрузки нового файла.
    """

    def render(self, name, value, attrs=None, renderer=None):
        """
        Отображает текущее изображение, если оно есть, и поле загрузки нового файла.
        """
        attrs = attrs or {}
        file_input = super().render(name, value, attrs, renderer)

        preview_html = ""
        if value and hasattr(value, "url"):
            preview_html = f"""
                <div class="image-preview-wrapper">
                    <div class="image-preview-box">
                        <img src="{value.url}" class="image-preview">
                        
                    </div>
                </div>
            """

        file_input_html = f"""
            <div class="image-upload-container">
                {file_input}
            </div>
        """

        return mark_safe(f'<div class="image-widget">{preview_html}{file_input_html}</div>')



class SetupForm(forms.ModelForm):
    text = forms.CharField(label='Текст на главной странице', required=False, widget=CKEditorUploadingWidget())

    class Meta:
        model = BaseSettings
        fields = [
            'name', 'ur_name', 'ur_address', 'inn', 'kpp', 'ogrn', 'okpo',
            'phone', 'phone_desc', 'email', 'email_for_order', 'telegram_bot', 'telegram_group',
            'sms_pilot_apikey', 'sms_text', 'api_geo', 'api_geocoder',
            'order_done_title', 'order_done_text', 'city', 'address', 'site_link', 'site_desc',
            'vk', 'vk_desc', 'whatsapp', 'whatsapp_desc', 'telegram', 'telegram_desc',
            'viber', 'viber_desc', 'ok', 'ok_desc', 'instagram', 'instagram_desc',
            'meta_title', 'meta_description', 'meta_keywords', 'meta_h1', 'text', 'social_image',
            'logo_dark', 'logo_height', 'logo_width', 'image_compression', 'icon_ico', 'icon_png', 'icon_svg',
            'pay_image', 'theme_color', 'active', 'hide_razrab_link', 'sms', 'debugging_mode'
        ]

        labels = {
            "name": "Название сайта",
            "ur_name": "Юридическое название",
            "ur_address": "Юридический адрес",
            "inn": "ИНН",
            "kpp": "КПП",
            "ogrn": "ОГРН",
            "okpo": "ОКПО",
            "phone": "Телефон",
            "phone_desc": "Описание телефона",
            "email": "Email для клиентов",
            "email_for_order": "Email для заявок",
            "telegram_bot": "Телеграм-бот (TOKEN)",
            "telegram_group": "Группа в Телеграме",
            "sms_pilot_apikey": "API ключ SMS Pilot",
            "sms_text": "Текст SMS при заказе",
            
            "order_done_title": "Заголовок при успешном заказе",
            "order_done_text": "Текст при успешном заказе",
            "city": "Город",
            "address": "Адрес",
            "site_link": "Ссылка на сайт",
            "site_desc": "Описание сайта",
            "vk": "Ссылка на VK",
            "vk_desc": "Описание VK",
            "whatsapp": "Ссылка на WhatsApp",
            "whatsapp_desc": "Описание WhatsApp",
            "telegram": "Ссылка на Telegram",
            "telegram_desc": "Описание Telegram",
            "viber": "Ссылка на Viber",
            "viber_desc": "Описание Viber",
            "ok": "Ссылка на Одноклассники",
            "ok_desc": "Описание Одноклассники",
            "instagram": "Ссылка на Instagram",
            "instagram_desc": "Описание Instagram",
            "meta_title": "Мета-заголовок",
            "meta_description": "Мета-описание",
            "meta_keywords": "Мета-ключевые слова",
            "meta_h1": "Заголовок H1",
            "text": "Текст на главной странице",
            "social_image": "Изображение для соцсетей",
            "logo_dark": "Логотип (темный)",
            "logo_height": "Высота логотипа",
            "logo_width": "Ширина логотипа",
            "image_compression": "Степень сжатия изображений",
            "icon_ico": "Иконка (.ico)",
            "icon_png": "Иконка (.png)",
            "icon_svg": "Иконка (.svg)",
            "pay_image": "Изображение способов оплаты",
            "theme_color": "Цветовая тема",
            "active": "Разрешить индексацию",
            "hide_razrab_link": "Скрыть ссылку на разработчика",
            "sms": "Разрешить SMS-уведомления",
            "debugging_mode": "Режим отладки"
        }

        widgets = {
            'social_image': ImagePreviewWidget(),
            'logo_dark': ImagePreviewWidget(),
            'icon_ico': ImagePreviewWidget(),
            'icon_png': ImagePreviewWidget(),
            'icon_svg': ImagePreviewWidget(),
            'pay_image': ImagePreviewWidget(),
            'theme_color': forms.TextInput(attrs={
               
                'placeholder': 'Цвет текста (не обязательно)',
                'type': 'color'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Группируем поля по секциям
        self.grouped_fields = {
            "company_info": ["name", "ur_name", "ur_address", "inn", "kpp", "ogrn", "okpo"],
            "contact_info": ["phone", "phone_desc", "email", "email_for_order", "telegram_bot", "telegram_group"],
            "sms_settings": ["sms_pilot_apikey", "sms_text"],
            "geo_settings": ["api_geo", "api_geocoder"],
            "order_settings": ["order_done_title", "order_done_text"],
            "address_info": ["city", "address"],
            "site_info": ["site_link", "site_desc"],
            "social_links": [
                "vk", "vk_desc", "whatsapp", "whatsapp_desc", "telegram", "telegram_desc",
                "viber", "viber_desc", "ok", "ok_desc", "instagram", "instagram_desc"
            ],
            "seo_settings": ["meta_title", "meta_description", "meta_keywords", "meta_h1"],
            "text_settings": ["text"],
            "design_settings": [
                "logo_dark", "logo_height", "logo_width", "image_compression",
                "icon_ico", "icon_png", "icon_svg", "pay_image", "social_image", "theme_color"
            ],
            "other_settings": ["active", "hide_razrab_link", "sms", "debugging_mode"]
        }

        # Добавляем CSS-классы для каждой группы
        for group, fields in self.grouped_fields.items():
            for field in fields:
                if field in self.fields:
                    widget = self.fields[field].widget
                    if not isinstance(widget, forms.CheckboxInput):  # Исключаем чекбоксы
                        widget.attrs.update({"class": f"input {group}"})
