from django.contrib import admin
from django.urls import path
from .views import register_user,authenticate_user, logout_user

app_name = "accounts"
urlpatterns = [
    path('register/',register_user ),
    path('login/',authenticate_user),
    path('logout/', logout_user, name="logout")   
]