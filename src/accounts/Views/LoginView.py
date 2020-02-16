from django.views import View
from django.template import loader
from django.contrib import messages
from utils.request import generate_url_for
from django.contrib.auth.models import User
from utils.koora import get_message_or_default
from django.contrib.auth import authenticate,login
from django.http import HttpResponse, HttpResponseRedirect
from utils.decorators import for_unauthenticated



class LoginView(View):



    @for_unauthenticated
    def get(self, request):

        if request.method =="GET":

            message = get_message_or_default(request, {})

            buffer = request.GET.dict()

            return HttpResponse(loader.get_template("accounts/login.html").render({
                'message' : message,
                'buffer' : buffer
            }, request))


    @for_unauthenticated
    def post(self, request):

        username=request.POST['username']
        password=request.POST['password']

        user = None

        try:
            user = User.objects.get(username=username)
        except:
            try:
                user = User.objects.get(email=username)
            except:
                pass


        if user and user.check_password(password):
            login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(generate_url_for('home'))

        else:
            return HttpResponseRedirect(generate_url_for("accounts:login", query={
                "type" : "danger",
                "content" : "Username or Password is not correct",
                "username" : username
            }))