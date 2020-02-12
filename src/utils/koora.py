from utils import uploader
from datetime import datetime
from django.urls import reverse
from articles.models import Tag
from django.conf import settings
from django.utils.http import urlencode
from django.contrib.auth.models import Permission


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


def setInterestsFor(user, interests):
    if len(interests) > 0:
        for interest in interests:
            legit_interest = interest.strip()
            if legit_interest:
                try:
                    existing_interest = Tag.objects.get(name=legit_interest)
                    user.profile.interests.add(existing_interest)
                except Tag.DoesNotExist:
                    user.profile.interests.create(name=legit_interest)


def uploadImageFor(model, image, key):
    key = "{}_{}.jpg".format(key, datetime.now())
    image_url = uploader.upload(image, key)
    model.image_url = image_url


def uploadAvatarImageFor(user, image, key):
    user.profile.avatar_url = uploader.upload(image, key)


def getKeyFromUrl(url):
    return url.split('/')[-1]


def deleteImageFor(model):
    if model.image_url:
        uploader.delete(getKeyFromUrl(model.image_url))


def deleteAvatarImageFor(user):
    if user.profile.avatar_url:
        uploader.delete(getKeyFromUrl(user.profile.avatar_url))


def getValueFor(reqKey, choices=settings.KOORA_CATEGORIES):
    values = {key: value for key, value in choices}
    try:
        return values[reqKey]
    except:
        return reqKey


def get_message_or_default(request, default):
    message_type = request.GET.get("type", False)
    message_content = request.GET.get("content", '')
    return {
        "type": message_type,
        "content": message_content
    } if message_type else default


def generate_url_for(*args, **kwargs):
    query = kwargs.pop('query', False)
    return reverse(*args, **kwargs) + (('?' + urlencode(query)) if query else '')


def premium_permission(method='add', user=None):

    can_upload_profile_picture = Permission.objects.get(
        codename='can_upload_profile_picture'
    )

    can_change_username = Permission.objects.get(
        codename='can_change_username'
    )

    can_make_profile_private = Permission.objects.get(
        codename='can_make_profile_private'
    )

    can_make_article_private = Permission.objects.get(
        codename='can_make_article_private'
    )

    can_draft_article = Permission.objects.get(
        codename='can_draft_article'
    )

    getattr(user.user_permissions, method)(
        can_upload_profile_picture,
        can_change_username,
        can_make_profile_private,
        can_make_article_private,
        can_draft_article
    )


def give_premium_to(user):
    premium_permission(method='add', user=user)


def remove_premium_from(user):
    premium_permission(method='remove', user=user)
