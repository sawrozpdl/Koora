from django.test import TestCase
from articles.models import Article
from django.contrib.auth.models import User

class ArticleTestCase(TestCase):

    admin = None


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

        # create one article with same title 't5'
        Article.objects.create(user=self.admin, title='t5', content='c6', category='RN')



    def test_create_count(self):

        self.set_environ()

        created_count = Article.objects.all().count()

        public_count = Article.objects.public().count()
        private_count = Article.objects.private().count()
        active_count = Article.objects.active().count()

        self.assertEqual(created_count, 6)

        self.assertEqual(public_count, 3)
        self.assertEqual(private_count, 2)
        self.assertEqual(active_count, 4)

    
    def test_user_access(self):

        self.set_environ()

        user = self.admin

        article_count = user.article_set.all().count()

        second_article_title = user.article_set.get(content="c2").title
        third_article_content = user.article_set.get(title="t3").content


        self.assertEqual(article_count,6)
        self.assertEqual(second_article_title, 't2')
        self.assertEqual(third_article_content, 'c3')


    def test_category(self):

        self.set_environ()

        food_category = 'FD'

        food_results = Article.objects.of_category(food_category)

        first_got_content = food_results[0].content

        self.assertEqual(first_got_content, 'c2')

    
    def test_attributes(self):
        
        self.set_environ()

        t1_article = Article.objects.get(title='t1')

        self.assertFalse(t1_article.is_drafted)

        t3_article = Article.objects.get(title='t3')

        self.assertTrue(t3_article.is_private)


        t1_slug = t1_article.slug

        self.assertEqual(t1_slug, 't1')


        t5_articles = Article.objects.filter(title='t5')

        first_t5_id = t5_articles[1].id 

        self.assertEqual(t5_articles[1].slug, 't5')
        self.assertEqual(t5_articles[0].slug, 't5-{}'.format(first_t5_id))
        


    def test_unique_slug(self):

        self.set_environ()

        t1_article = Article.objects.get(title='t1')
        t2_article = Article.objects.get(title='t2')
        t3_article = Article.objects.get(title='t3')

        self.assertNotEqual(t1_article.slug, t2_article.slug)
        self.assertNotEqual(t2_article.slug, t3_article.slug)



    def test_functions(self):

        self.set_environ()

        self.assertEquals(str(Article.objects.get(title='t1')), 't1')




