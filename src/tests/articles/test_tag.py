from django.test import TestCase
from articles.models import Article, Tag
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

        a1 = Article.objects.create(user=self.admin, title='t1', content='c1', category='RN', is_private=True)
        a2 = Article.objects.create(user=self.admin, title='t2', content='c2', category='FD', is_drafted=True)
        a3 = Article.objects.create(user=self.admin, title='t3', content='c3', category='AR', is_private=True, is_drafted=True)
        a4 = Article.objects.create(user=self.admin, title='t4', content='c4', category='GM')
        a5 = Article.objects.create(user=self.admin, title='t5', content='c5', category='PH')

        t1 = Tag.objects.create(name='tag1')
        t2 = Tag.objects.create(name='tag2')


        #adding tags to each articles
        a1.tags.add(t1)
        a2.tags.add(t1)
        a3.tags.add(t1)
        a4.tags.add(t2)
        a5.tags.add(t2)

    def test_creation(self):

        self.set_environ()

        all_tags = Tag.objects.all()

        tags_count = all_tags.count()

        self.assertEqual(tags_count, 2)
        self.assertEqual(all_tags[0].name, 'tag1')


    def test_article_access(self):

        self.set_environ()

        t1 = Tag.objects.get(name='tag1')
        t2 = Tag.objects.get(name='tag2')

        a1 = Article.objects.get(title='t1')
        a5 = Article.objects.get(title='t5')

        t1_articles = t1.get_associated_articles()
        t2_articles = t2.get_associated_articles()


        self.assertGreater(t1_articles.count(), t2_articles.count())

        self.assertTrue(a1 in list(t1_articles))
        self.assertTrue(a5 in list(t2_articles))
        self.assertFalse(a5 in list(t1_articles))



    def test_functions(self):

        self.set_environ()

        t1 = Tag.objects.get(name='tag1')

        self.assertEqual(str(t1), 'tag1')



