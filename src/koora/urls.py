from django.contrib import admin
from django.urls import path
from .views import hello, read_file, search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('read/<slug:filename>',read_file),
    



]
