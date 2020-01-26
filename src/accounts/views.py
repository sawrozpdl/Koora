from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.urls import reverse
from django.template import loader

# from accounts.models import Profile

def user_profile(request):
    return render(request,'../templates/profile/profile.html')
    if user.object.type() == 'premium':
        


# def get(delf,request):
#     pro = profile.objects.all()
#     required_articles = list(filter(lambda article : article.contains_user(searchQuery), Article.objects.all()))




# Create your views here.
def register_user(request):
    if request.method =="GET":
        return HttpResponse(loader.get_template("accounts/register.html").render({}, request))
    else:
        print(request.POST)
        user = User.objects.create_user(username=request.POST['username'],password=request.POST['f_password'],email=request.POST['email'])
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
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        print(user)
        if user is not None:
            login(request,user)
            content = {
            "page_name": "login",
            "messages" : [
                {
                    "type" : "success",
                    "content" : "Login Successfull!"
                }
            ],
        }
            return HttpResponse(loader.get_template("base.html").render(content, request))
        else:
            HttpResponseForbidden()

def logout_user(request):
    if (not request.user.is_authenticated):
        return HttpResponseForbidden('You cant be here')
    logout(request)
    return HttpResponseRedirect(reverse('home'))
