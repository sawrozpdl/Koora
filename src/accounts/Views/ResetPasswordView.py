from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from utils.request import generate_url_for



def reset_password(request): 
    send_mail('Password reset request', 
    'you have sent request',
    'dipeshlama4869@gmail.com',
    ['user.email'], 
    fail_silently = False)
    return HttpResponse(loader.get_template("accounts/change_password.html").render({}, request))

def change_password(request):
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    
    if new_password != confirm_password:
        return HttpResponseRedirect(generate_url_for("accounts/change_password.html", query={
                "type" : "danger",
                "content" : "Password doesn't match"
            }))
    else:
        return HttpResponseRedirect(generate_url_for('account:Login'))
