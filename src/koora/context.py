from django.conf import settings
from articles.models import Tag



def interceptor(request):
    popular_tags = Tag.objects.all()
    categories = settings.KOORA_CATEGORIES
    return {
        'popular_tags' : popular_tags,
        'categories' : categories
    }