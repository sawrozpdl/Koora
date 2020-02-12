from django.urls import path
from django.conf.urls import include
from .views import SettingsView, ProfileView

app_name = 'user'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<slug:username>', ProfileView.as_view(), name='visitprofile'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
