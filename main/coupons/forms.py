from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField()

    code = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'cart-total__input',
        'placeholder': 'Код купона'
        }))