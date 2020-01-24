from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from .views import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls', namespace='articles'), name='articles'),
    path('', index, name='home'),

    # path('accounts/', include('accounts.urls'))    

    path('accounts/', include('accounts.urls', namespace='accounts'), name='accounts'),

    path('comments/', include('comments.urls', namespace='comments'), name='comments'),
    
    path('', index, name='home')
]
