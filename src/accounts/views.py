from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.
def register_user(request):
    if request.method =="GET":
        return render(request,'../templates/accounts/accounts/register.html')
    else:
        print(request.POST)
        user = User.objects.create_user(username=request.POST['uname'],password=request.POST['pass'],email=request.POST['mail'])
        user.save()
        return HttpResponse("Signup Successful")


def authenticate_user(request):
    if request.method =="GET":
        return render (request,'../templates/accounts/accounts/login.html')
    else:
        print(request.POST)
        user = authenticate(username=request.POST['uname'],password=request.POST['pass'])
        print(user)
        if user is not None:
            login(request,user)
            return render(request,"../templates/base.html")
        else:
            return HttpResponse("Authentication Failed")  
