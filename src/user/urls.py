from django.urls import path
from django.conf.urls import include
from .views import SettingsView

app_name = 'user'

urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings'),
]
