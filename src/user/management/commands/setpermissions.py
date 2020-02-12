from django.core.management import BaseCommand

from articles.models import Article
from user.models import Profile

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):


    def handle(self, *args, **options):

        self.stdout.write("Setting required permissions....")

        article_content_type = ContentType.objects.get_for_model(Article)
        profile_content_type = ContentType.objects.get_for_model(Profile)

        try:
            can_upload_profile_picture = Permission.objects.create(
                codename='can_upload_profile_picture',
                name='Can upload avatar images for profile',
                content_type=profile_content_type,
            )

            can_change_username = Permission.objects.create(
                codename='can_change_username',
                name='Can change username',
                content_type=profile_content_type,
            )

            can_make_profile_private = Permission.objects.create(
                codename='can_make_profile_private',
                name='Can set the profile to private',
                content_type=profile_content_type,
            )

            can_make_article_private = Permission.objects.create(
                codename='can_make_article_private',
                name='Can make private posts for articles',
                content_type=article_content_type,
            )

            can_draft_article = Permission.objects.create(
                codename='can_draft_article',
                name='Can draft any article',
                content_type=article_content_type,
            )
        except:
            self.stdout.write("Already Set!")

        self.stdout.write("Done!")

