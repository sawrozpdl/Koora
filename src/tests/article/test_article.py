from django.test import TestCase

class ArticleTestCase(TestCase):

    def test_addition(self):
        self.assertEqual(4, 5)
        self.assertEqual(4, 4)