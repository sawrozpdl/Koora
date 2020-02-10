from django.urls import path

from .views import CreateView, ListView

app_name = 'questions'

urlpatterns = [
     path('', ListView.as_view(), name='list'),
     path('create', CreateView.as_view(), name='create'),

]
