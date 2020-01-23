from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
def register_user(request):
    if request.method =="GET":
        return render(request,'../templates/accounts/accounts/register.html')
    else:
        print(request.POST)
        user = User.objects.create_user(username=request.POST['uname'],password=request.POST['pass'],email=request.POST['mail'])
        user.save()
        return HttpResponseRedirect(reverse('home'))


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


def logout_user(request):
    if (not request.user.is_authenticated):
        return HttpResponseForbidden('You cant be here')
    logout(request)
    return HttpResponseRedirect(reverse('home'))