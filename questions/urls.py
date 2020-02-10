from django.urls import path

from .views import CreateView, ListView, DetailView


app_name = 'questions'

urlpatterns = [
     path('', ListView.as_view(), name='list'),
     path('create', CreateView.as_view(), name='create'),
     path('detail', DetailView.as_view(), name='detail'),



]
