from .models import BaseSettings, CustomCode, Colors, Fonts, ThemeSettings
from delivery.models import Delivery

def setup(request):
    try:
        setup = BaseSettings.objects.get()
    except:
        setup = []
    return {'setup': setup}


def codes(request):
    try:
        codes = CustomCode.objects.all()
    except:
        codes = []
    return {'codes': codes}


def colors(request):
    try:
        colors = Colors.objects.get()
    except:
        colors = []
    return {'colors': colors}


def theme(request):
    try:
        theme = ThemeSettings.objects.get()
    except:
        theme = []
    return {'theme': theme}

def fonts(request):
    try:
        font = Fonts.objects.get()
    except:
        font = Fonts.objects.create()
        
    return {'font': font}


def delivery(request):
    try:
        delivery_object = Delivery.objects.get()
        delivery = delivery_object.active
    except:
        delivery = None
    return {'delivery': delivery}