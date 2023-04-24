from django.shortcuts import render

# Create your views here.
import requests
from setup.models import BaseSettings

try:
    sms = BaseSettings.objects.get().sms
    apikey = BaseSettings.objects.get().sms_pilot_apikey
except:
    sms = False
    apikey = 'BS0H0F27LS92CU4G3YVZQ693A1QGCTQT2DBOF2NDKMB99465LQSU8O7RPU084Y60'


def send_sms(text, phone):
    url = "http://smspilot.ru/api.php?send="+text+"&to="+phone+"&apikey="+apikey+"&format=json"
    if sms == True:
        # pass
        result = requests.get(url)
