from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'postal_code', 'city']

        widgets = {
           
            'first_name': forms.TextInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Имя',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Фамилия',
                'required': 'required'

            }),
            'phone': forms.NumberInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Телефон',
                'required': 'required'

            }),
            'email': forms.TextInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'E-mail'
            }),
            'address': forms.TextInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Адрес'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Индекс'
            }),
            'city': forms.TextInput(attrs={
                'class': 'order-detail__input',
                'placeholder': 'Город'
            }),
        }