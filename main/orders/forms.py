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
           
            'address',
            
            ]

        widgets = {
           
            
            'phone': forms.NumberInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Телефон',
                'required': 'required'

            }),
           
            'address': forms.TextInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Адрес',
                'required': 'required'
            })
            
           
        }