from django.shortcuts import render

# Create your views here.
import requests
from setup.models import BaseSettings

sms = BaseSettings.objects.get().sms

sender = 'INFORM'
apikey = 'BS0H0F27LS92CU4G3YVZQ693A1QGCTQT2DBOF2NDKMB99465LQSU8O7RPU084Y60'


def send_sms(text, phone):
    url = "http://smspilot.ru/api.php?send="+text+"&to="+phone+"&from="+sender+"&apikey="+apikey+"&format=json"
    if sms == True:
        result = requests.get(url)
