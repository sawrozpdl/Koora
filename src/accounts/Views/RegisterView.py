from django.views import View
from django.urls import reverse
from django.template import loader
from django.contrib import messages
from utils.request import generate_url_for
from django.contrib.auth.models import User
from utils.koora import get_message_or_default
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from utils.decorators import for_unauthenticated

class RegisterView(View):


    @for_unauthenticated
    def get(self, request):
        if request.method =="GET":
            message = get_message_or_default(request, {})
            buffer = request.GET.dict()
            return HttpResponse(loader.get_template("accounts/register.html").render({
                "message" : message,
                "buffer" : buffer
            }, request))



    @for_unauthenticated
    def post(self, request):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['f_password']
        confirm_password=request.POST['r_password']

        if User.objects.filter(username=username).exists():

            return HttpResponseRedirect(generate_url_for("accounts:register", query={
                "type" : "danger",
                "content" : "Username is already taken",
                'username' : username,
                'email' : email
            }))

        if User.objects.filter(email=email).exists():

            return HttpResponseRedirect(generate_url_for("accounts:register", query={
                "type" : "danger",
                "content" : "Email is already taken",
                'username' : username,
                'email' : email
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