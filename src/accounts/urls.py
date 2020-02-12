from django.contrib import admin
from django.urls import path
from .Views import (RegisterView, LoginView, LogoutView, ChangePasswordView, ResetPasswordView)

app_name = "accounts"

urlpatterns = [
    path('register/',RegisterView.as_view(), name="register"),
    path('login/',LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('reset/', ResetPasswordView.as_view(), name="reset"),
    path('forgot/', ChangePasswordView.as_view(), name="forgot")
]