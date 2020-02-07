from django.urls import path
from django.conf.urls import include
from .views import logout


app_name = 'auth-api'

urlpatterns = [
    path('logout', logout, name='logout'),
]
