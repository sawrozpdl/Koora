from django.urls import reverse
from django.template import loader
from django.shortcuts import render
from django.contrib import messages
from utils.request import generate_url_for
from django.contrib.auth.models import User
from utils.koora import get_message_or_default
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden


def register_user(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method =="GET":

        message = get_message_or_default(request, {})

        return HttpResponse(loader.get_template("accounts/register.html").render({
            "message" : message
        }, request))

    else:
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['f_password']
        confirm_password=request.POST['r_password']

    if User.objects.filter(username=username).exists():

        return HttpResponseRedirect(generate_url_for("accounts:register", query={
            "type" : "danger",
            "content" : "Username is already taken"
        }))


    if password != confirm_password:

        return HttpResponseRedirect(generate_url_for("accounts:register", query={
            "type" : "danger",
            "content" : "Password doesn't match"
        }))

    else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return HttpResponseRedirect(generate_url_for("accounts:login", query={
            "type" : "success",
            "content" : "Signup Successfull, You may now login"
        }))


def authenticate_user(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method =="GET":

        message = get_message_or_default(request, {})
        
        return HttpResponse(loader.get_template("accounts/login.html").render({
            'message' : message
        }, request))

    else:

        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('home'))

        else:
            return HttpResponseRedirect(generate_url_for("accounts:login", query={
                "type" : "danger",
                "content" : "Username or Password is not correct"
            }))


def logout_user(request):

    if (not request.user.is_authenticated):
        return HttpResponseForbidden('You cant be here')

    logout(request)

    response = HttpResponseRedirect(reverse('home'))

    response.delete_cookie('accessToken')

    return response