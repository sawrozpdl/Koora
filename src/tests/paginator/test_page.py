from django.test import TestCase
from utils.pages import Page


class PageTestCase(TestCase):

    list1 = [2, 3, 4, 5]
    list2 = [5, 6, 8, 2]

    page1 = Page(list1, 0)
    page2 = Page(list2, 4)

    page1.next_page = page2
    page2.previous_page = page1
    
    def test_placement(self):
        self.assertTrue(self.page1.has_next())
        self.assertFalse(self.page1.has_previous())
        self.assertTrue(self.page2.has_previous())
        self.assertFalse(self.page2.has_next())

    

    def test_content(self):
        self.page2.page_number = 2
        self.assertEquals(self.page1.next_page_number(), 2)
        self.assertEquals(self.page1.next_page.previous_page.object_list, self.list1)