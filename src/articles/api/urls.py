from django.urls import path
from django.conf.urls import include
from .views import (ListAPIView, DetailAPIView, VoteAPIView)

app_name = 'articles-api'

urlpatterns = [
    path('', ListAPIView.as_view(), name='list'),
    path('vote', VoteAPIView.as_view(), name='vote'),
    path('<slug:slug>', DetailAPIView.as_view(), name='detail'),
]
