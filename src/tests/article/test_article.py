from django.test import TestCase

class ArticleTestCase(TestCase):

    def addition_test(self):
        self.assertEqual(5, 5)
        self.assertEqual(3, 3)