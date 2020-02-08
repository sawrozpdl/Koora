from django.test import TestCase
from comments.models import Comment
from articles.models import Article
from django.contrib.auth.models import User

class CommentTestCase(TestCase):

    admin = None

    def set_up_user(self):
        user=User.objects.create_user('saroj', password='Saw123@##')
        user.is_superuser=True
        user.is_staff=True
        user.save()

        self.admin = user

    def set_environ(self):

        self.set_up_user()

        a1 = Article.objects.create(user=self.admin, title='a1', content='article1', category='RN')

        article_content_type = a1.content_type

        # add comment to a1 : Article
        c1 = Comment.objects.create(user=self.admin, content='a1c1', object_id=a1.id, content_type=article_content_type)
        c2 = Comment.objects.create(user=self.admin, content='a1c2', object_id=a1.id, content_type=article_content_type)

        # add comments to c2 : Comment
        c3 = Comment.objects.create(user=self.admin, content='c2c3', object_id=a1.id, content_type=article_content_type, parent=c2)
        c4 = Comment.objects.create(user=self.admin, content='c2c4', object_id=a1.id, content_type=article_content_type, parent=c2)

        # add commnent to c4 : Comment
        c5 = Comment.objects.create(user=self.admin, content='c4c5', object_id=a1.id, content_type=article_content_type, parent=c4)



    def test_create_count(self):

        self.set_environ()

        a1 = Article.objects.get(title='a1')

        a1_total_comments = a1.all_comments

        a1_comments = a1.comments.count()

        self.assertEqual(a1_total_comments, 5)
        self.assertEqual(a1_comments, 2)

        c2 = Comment.objects.get(content='a1c2')

        c2_replies = c2.children.count()

        self.assertEqual(c2_replies, 2)



    def test_comment_thread(self):

        self.set_environ()


        c2 = Comment.objects.get(content='a1c2')

        c2_replies = c2.children

        first_reply = c2_replies[0]

        self.assertEquals(c2, first_reply.parent)


        second_reply = c2_replies[1]

        self.assertEqual(second_reply.content, 'c2c4')


        third_level_nested_reply = second_reply.children[0]
        expected_reply = Comment.objects.get(content='c4c5')

        self.assertEquals(third_level_nested_reply, expected_reply)



    def test_functions(self):

        self.set_environ()

        c1 = Comment.objects.get(content='a1c1')

        username = self.admin.username

        self.assertEquals(str(c1), username)




