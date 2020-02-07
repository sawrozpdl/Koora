from utils import uploader
from datetime import datetime
from django.urls import reverse
from articles.models import Tag
from django.conf import settings
from django.utils.http import urlencode

def setTagsFor(model, tags):
    if len(tags) > 0:
        for tag in tags:
            legit_tag = tag.strip()
            if legit_tag:
                try:
                    existing_tag = Tag.objects.get(name=legit_tag)
                    model.tags.add(existing_tag)
                except Tag.DoesNotExist:
                    model.tags.create(name=legit_tag)

def uploadImageFor(model, image, key):
    key = "{}_{}.jpg".format(key, datetime.now())
    image_url = uploader.upload(image, key)
    model.image_url = image_url


def getKeyFromUrl(url): 
    return url.split('/')[-1]


def deleteImageFor(model):
    if model.image_url:
        uploader.delete(getKeyFromUrl(model.image_url))


def getValueFor(reqKey, choices=settings.KOORA_CATEGORIES):
    values = {key : value for key, value in choices}
    return values[reqKey]


def get_message_or_default(request, default):
    message_type = request.GET.get("type", False)
    message_content = request.GET.get("content", '')
    return {
        "type" : message_type,
        "content" : message_content
    } if message_type else default


def generate_url_for(*args, **kwargs):
    query = kwargs.pop('query', False)
    return reverse(*args, **kwargs) + (('?' + urlencode(query)) if query else '')