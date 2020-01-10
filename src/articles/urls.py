from django.urls import path

from .views import (create, update, list, detail)

app_name = 'articles'

urlpatterns = [
    path('', list.ListView.as_view(), name='list'),
    path('create', create.CreateView.as_view(), name='create'),
    path('<slug:article_id>', detail.DetailView.as_view(), name='detail'),
    path('update/<slug:article_id>', update.UpdateView.as_view(), name='update')
]
