from django.test import TestCase
from django.test import TestCase
from articles.models import Article
from django.contrib.auth.models import User


class TagTestCase(TestCase):

    def set_up_user(self):
        user=User.objects.create_user('saroj', password='Saw123@##')
        user.is_superuser=True
        user.is_staff=True
        user.save()

        self.admin = user

    def set_environ(self):
        self.set_up_user()

        Article.objects.create(user=self.admin, title='t1', content='c1', category='RN', is_private=True)
        Article.objects.create(user=self.admin, title='t2', content='c2', category='FD', is_drafted=True)
        Article.objects.create(user=self.admin, title='t3', content='c3', category='AR', is_private=True, is_drafted=True)
        Article.objects.create(user=self.admin, title='t4', content='c4', category='GM')
        Article.objects.create(user=self.admin, title='t5', content='c5', category='PH')

        Article.objects.create(user=self.admin, title='t5', content='c6', category='RN')