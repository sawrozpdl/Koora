from django.contrib import admin
from django.urls import path
from .views import register_user,authenticate_user

urlpatterns = [
    path('register/',register_user ),
    path('login/',authenticate_user )
    
]