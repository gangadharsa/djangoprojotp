from django.shortcuts import render
from django.http import HttpResponse
from .models import Reg
from .forms import LoginForm
from .forms import RegForm
from django.core.mail import send_mail
from django.conf import settings
import random
import http
import json
def home(request):
    return render(request,'home.html')
def reg(request):
        if request.method == 'POST':
           regform = RegForm(request.POST)
           if regform.is_valid():
               x=otp_send(request)
               if x:
                   return render(request,'otp_input.html')
               else:
                   return render(request,'reg.html',{'regform': regform})
           else:
               return render(request, 'reg.html',{'regform': regform})
        else:
          regform = RegForm()
          return render(request,'reg.html',{'regform': regform})
def otpvalidation(request):
    newotp=request.POST["otp"]
    oldotp=request.session["otp"]
    if newotp==oldotp:
        form=RegForm(request.session["details"])
        form.save()
        return HttpResponse("registration success")
    else:
        return render(request,'otp_input.html')

def login(request):
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            un =loginform.cleaned_data['username']
            pw=loginform.cleaned_data['password']
            dbuser = Reg.objects.filter(username=un,password=pw)
            if not dbuser:
                return HttpResponse('login faild')
            else:
                return HttpResponse('login success')
    else:
        loginform = LoginForm()
        return render(request,'login.html',{'loginform': loginform})




def otp_send(request):
    ot = str(random.randint(100000, 999999))
    # request.session["pwd"]=request.POST["t1"]
    mobno = request.POST["mobno"]
    temail=request.POST["emailid"]
    subject="registration otp"
    From_mail = settings.EMAIL_HOST_USER
    to_list = [temail]

    send_mail(subject, ot, From_mail, to_list, fail_silently=False)
    print("otp sent to email")
    request.session["details"] = request.POST
    request.session["otp"] = ot
    conn = http.client.HTTPConnection("api.msg91.com")
    payload = "{ \"sender\":\"LKSHIT\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\":\"" + ot + "\",\"to\": [ \"" + mobno + "\" ] } ] }"
    headers = {
        'authkey': "274645AEocCOqFlqb5cc8a8ac",  # PLEASE ENTER THE AUTHKEY BEFORE EXECUTING THE PROGRAM
        'content-type': "application/json"
    }

    conn.request("POST",
                 "/api/v2/sendsms?country=91&sender=&route=&mobiles=&authkey=&encrypt=&message=&flash=&unicode=&schtime=&afterminutes=&response=&campaign=",
                 payload, headers)

    data = conn.getresponse()
    res = json.loads(data.read().decode("utf-8"))
    print(res)
    if res["type"] == "success":
        return True
    else:
        return False

# Create your views here.
