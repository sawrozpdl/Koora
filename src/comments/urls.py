from django.urls import path

from .views import (ListView, DetailView)

app_name = 'comments'

urlpatterns = [
    path('<slug:model>', ListView.as_view(), name='list'),
    path('<slug:model>/<slug:slug>', DetailView.as_view(), name='detail')
]
