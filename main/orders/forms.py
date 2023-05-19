from django import forms
from .models import Order

from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class CallbackForm(forms.Form):
    # captcha = ReCaptchaField()
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'popup__input', 'placeholder': 'Имя'}))
    phone = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'popup__input phone', 'placeholder': 'Телефон'}))
    messages = forms.CharField(label='',widget=forms.Textarea(attrs={'class': 'popup__input', 'placeholder': 'Сообщение'}))



class OrderCreateForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Order
        fields = [

            'phone',
            'address',
            'address_comment',
            'entrance',
            'floor',
            'flat',
            'time',
            'order_conmment',
            'captcha',
            'delivery_method',
            'pay_method',
            'address',
            
            ]

        widgets = {
           
            
            'phone': forms.NumberInput(attrs={
                'class': 'order-detail__input phone',
                'placeholder': 'Телефон',
                'required': 'required'

            }),
           
            'address': forms.TextInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Адрес',
                'required': 'required'
            })
            
           
        }