from django.shortcuts import render, redirect


import random
import datetime



def  get_code():
    random.seed()
    return str(random.randint(10000,99999))


    



def code(request):

    if request.method == 'POST':

        session = request.session
        session["code"] = str(get_code())
        session["code_date"] = str(datetime.datetime.now())

        code = session["code"]
        code_date = session["code_date"]
        print(code, code_date)

        return redirect('/')
    
    else:

        return redirect('/')