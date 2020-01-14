from django.test import TestCase

class ArticleTestCase(TestCase):

    def test_animals_can_speak(self):
        self.assertEqual(5, 5)
        self.assertEqual(3, 3)