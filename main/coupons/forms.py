from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class CouponApplyForm(forms.Form):
    code = forms.CharField()
    captcha = ReCaptchaField()

    code = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'cart__input',
        'placeholder': 'Код купона'
        }))