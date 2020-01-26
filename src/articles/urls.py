from django.urls import path
from django.conf.urls import include
from .views import (CreateView, UpdateView, ListView, DetailView, VoteView)

app_name = 'articles'

urlpatterns = [
    path('', ListView.as_view(), name='list'),
    path('create', CreateView.as_view(), name='create'),
    path('vote', VoteView.as_view(), name='vote'),
    path('<slug:slug>', DetailView.as_view(), name='detail'),
    path('update/<slug:slug>', UpdateView.as_view(), name='update')
]
