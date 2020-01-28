from django.contrib import admin
from django.urls import path
from .views import user_profile
from .views import register_user,authenticate_user, logout_user


app_name = "accounts"
urlpatterns = [
    path('profile/',user_profile, name='profile'),
    # url(r'^user/(?P<username>[-\w.]+)/$', views.user_profile.as_view(), name='user_profile'),
    path('register/',register_user, name="register"),
    path('login/',authenticate_user, name="login"),
    path('logout/', logout_user, name="logout")   
]
