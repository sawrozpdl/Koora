from django.test import TestCase
from articles.models import Article, Vote
from django.contrib.auth.models import User

class VoteTestCase(TestCase):

    def set_up_user(self):
        user=User.objects.create_user('saroj', password='Saw123@##')
        user.is_superuser=True
        user.is_staff=True
        user.save()

        self.admin = user

    def vote(self, content_obj, count, upvote=True):

        content_type = content_obj.content_type

        for c in range(0, count):
            Vote.objects.create(user=self.admin, is_upvote=upvote, content_type=content_type, object_id=content_obj.id)


    def set_environ(self):
        self.set_up_user()

        a1 = Article.objects.create(user=self.admin, title='t1', content='c1', category='RN')
        a2 = Article.objects.create(user=self.admin, title='t2', content='c2', category='FD')

        self.vote(a1, 10)
        self.vote(a2, 21)


    def test_voting(self):

        self.set_environ()

        a1 = Article.objects.get(title='t1')

        self.assertEqual(a1.vote_count, 10)

        # downvoting article 'a1'
        self.vote(a1, 3, False) 

        self.assertEqual(a1.vote_count, 7)


        self.vote(a1, 10, False)

        self.assertEqual(a1.vote_count, -3)



    def test_vote_type(self):

        self.set_environ()

        a1 = Article.objects.get(title='t1')

        self.vote(a1, 5, False) 

        vote1 = a1.up_votes[0]

        vote2 = a1.down_votes[0]


        self.assertTrue(vote1.vote_type_for(self.admin))    # i.e upvote
        self.assertFalse(vote2.vote_type_for(self.admin))   # i.e downvote

        random_user = User.objects.create_user('sahil', password='Sadfss23@##')

        self.assertEqual(vote1.vote_type_for(random_user), -1) # i.e no vote


        