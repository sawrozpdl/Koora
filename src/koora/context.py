from django.conf import settings
from articles.models import Tag


def interceptor(request):
    tags = Tag.objects.all()
    popular_tags = sorted(tags, key = lambda tag : tag.associated_count, reverse = True)[:10]
    categories = settings.KOORA_CATEGORIES
    countries = settings.COUNTRIES
    return {
        'popular_tags' : popular_tags,
        'categories' : categories,
        'countries' : countries
    }