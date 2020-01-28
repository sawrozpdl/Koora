from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.urls import reverse
from django.template import loader
from django.contrib import messages




# from accounts.models import Profile

def user_profile(request):
    return render(request,'../templates/profile/profile.html')



# Create your views here.
def register_user(request):
    if request.method =="GET":
        return HttpResponse(loader.get_template("accounts/register.html").render({}, request))
        

    else:
        print(request.POST)
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['f_password']
        confirm_password=request.POST['r_password']


    if User.objects.filter(username=username).exists():
        return HttpResponse(loader.get_template("accounts/register.html").render({
            "messages" : [
                {
                    "type" : "danger",
                    "content" : "Username is already taken"
                }
            ],
        }, request))
    if password != confirm_password:
        return HttpResponse(loader.get_template("accounts/register.html").render({
        "messages" : [
            {
                "type" : "danger",
                "content" : "Password doesn't match"
            }
        ],               
        }, request))    
    else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()


        content = {
            "page_name": "login",
            "messages" : [
                {
                    "type" : "success",
                    "content" : "Signup Successfull, You may now login"
                }
            ],
        }
        return HttpResponse(loader.get_template("accounts/login.html").render(content, request))


def authenticate_user(request):
    if request.method =="GET":
        return HttpResponse(loader.get_template("accounts/login.html").render({}, request))
    else:
        print(request.POST)
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        #print(user)
        if user:
            login(request,user)
            content = {
            "page_name": "login"
        }
            return HttpResponse(loader.get_template("base.html").render(content, request))
        else:
            content = {
                "page_name": "authentication fail",
                "messages" : [
                    {
                        "type" : "danger",
                        "content" : "Username or Password is not correct"
                    }
                ]            
            }
            return HttpResponse(loader.get_template("accounts/login.html").render(content, request))

def logout_user(request):
    if (not request.user.is_authenticated):
        return HttpResponseForbidden('You cant be here')
    logout(request)
    return HttpResponseRedirect(reverse('home'))
