from django.urls import path
from django.conf.urls import include
from .views import DetailAPIView

app_name = 'comments-api'

urlpatterns = [
    path('<slug:slug>', DetailAPIView.as_view(), name='detail'),
]
