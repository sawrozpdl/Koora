from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('articles/', include('articles.urls', namespace='articles'), name='articles'),
    path('accounts/', include('accounts.urls', namespace='accounts'), name='accounts'),
    path('comments/', include('comments.urls', namespace='comments'), name='comments'),
    path('user/', include('user.urls', namespace='user'), name='user'),


    path('api/articles/', include('articles.api.urls', namespace='articles-api'), name='aritcles-api'),
    path('api/comments/', include('comments.api.urls', namespace='comments-api'), name='comments-api'),
    path('api/auth/', include('authentication.urls', namespace='auth-api'), name='auth-api')

]
