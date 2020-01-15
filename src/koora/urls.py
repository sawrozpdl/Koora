from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from .views import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls', namespace='articles'), name='articles'),
    path('', index, name='home')
]


if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)