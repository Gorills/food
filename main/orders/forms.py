from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
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