from utils import uploader
from datetime import datetime
from articles.models import Tag


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
    key = "%s_%s.jpg" % (key, datetime.now())
    image_url = uploader.upload(image, key)
    model.image_url = image_url


def getKeyFromUrl(url): 
    return url.split('/')[-1]


def deleteImageFor(model):
    uploader.delete(getKeyFromUrl(model.image_url))