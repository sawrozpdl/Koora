from django.views import View
from django.template import loader
from django.contrib import messages
from utils.request import generate_url_for
from django.contrib.auth.models import User
from utils.koora import get_message_or_default
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


class LogoutView(View):
    
    def get(self, request):
        
        logout(request)

        return HttpResponseRedirect(generate_url_for('auth-api:logout'))

    def post(self, request):
        pass