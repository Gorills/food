
# Странная отправка СМС
import datetime

import random
import requests

def generate_code():
    random.seed()
    
    return str(random.randint(10000,99999))

phone = '79528984601'
text = 'Код доступа'
sender = 'INFORM'
apikey = 'BS0H0F27LS92CU4G3YVZQ693A1QGCTQT2DBOF2NDKMB99465LQSU8O7RPU084Y60'
url = "http://smspilot.ru/api.php?send="+'Ваш код:'+generate_code()+"&to="+phone+"&from="+sender+"&apikey="+apikey+"&format=json"

def send_sms():
    response = requests.get(url)
    print(url)

# send_sms()

def send_code(request):
    user = request.user
    session = request.session
    gen_code = True
    code = ""
    if 'code' in session and 'code_date' in session:
        if int((datetime.datetime.now() - session['code_date']).total_seconds())< 180:
            code = session['code']
            gen_code=False
 
    if gen_code:
        session["code"] = generate_code()
        session["code_date"] = datetime.datetime.now()
        code = session["code"]
 
    send = True
    if send:
        url = "http://smspilot.ru/api.php?send="+'Ваш код: '+generate_code()+"&to="+phone+"&from="+sender+"&apikey="+apikey+"&format=json"
        result = requests.get(url)
        try:
            if int(result['send'][0]['status']) == 0:
                return True
        except:
            pass
        return False
    else:
        print("Phone: %s, code %s" %(user.get_profile().phone, code))
        return True

# Странная отправка СМС