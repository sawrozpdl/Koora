from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls', namespace='articles'), name='articles'),
    path('', index, name='home'),
    path('accounts/', include('accounts.urls'))
]
