


import requests
import os



# кодирование параметров запроса в URL-формат
login = "shopds7k"
password = "Ie51587v!"



import os

def get_folder(path):
    # current_dir = str(os.getcwd())
    current_dir = path


    print(current_dir)

    folder_list = current_dir.split('/')
    folder = ''
    set_foder = False
    for f in folder_list:
        if f == 'shopds7k':
            set_foder = True
            continue
        if set_foder:
            folder = f
            set_foder = False

    return folder
   
# folder = get_folder('/home/s/shopds7k/shavuha-i-ne-tolko/public_html')
# print(folder)

import json
import json
import requests
from urllib.parse import urlencode

def set_cron(slug, minutes, hours):
    command = f'ssh localhost -p222 "source /home/s/shopds7k/{slug}/public_html/venv/bin/activate && python /home/s/shopds7k/{slug}/public_html/main/manage.py sync"'

    if minutes == '0': 
        m = '*'
    else:
        m = minutes
    if hours == '0':
        h = '*'
    else:
        h = hours

    input_data = {
        "minutes": f"/{m}",
        "hours": f"/{h}",
        "days": "*",
        "months": "*",
        "weekdays": "*",
        "command": command
    }

    input_data_json = json.dumps(input_data)

    # экранируем специальные символы в строке запроса
    params = urlencode({
        "login": login,
        "passwd": password,
        "input_format": "json",
        "output_format": "json",
        "input_data": input_data_json
    })

    cron_url = f'https://api.beget.com/api/cron/add?{params}'

    response = requests.post(cron_url)
    response_json = json.loads(response.content.decode('utf-8'))
    print(response_json)
    

# set_cron('demo', "0", "1")