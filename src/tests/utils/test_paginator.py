from django.test import TestCase
from utils.pages import Paginator


class PaginationTestCase(TestCase):

    data = [11, 21, 34, 4, 35,    
            6, 7, 8, 79, 10,      
            32, 12, 20, 3, 12,    
            12, 23, 45, 25, 56,   
            23, 54, 6, 8, 87,     
            87, 5, 443, 223, 4,   
            41, 22, 34]           

    pages = Paginator(data, 5)

    def test_population(self):
        self.assertEquals(self.pages.page(3).object_list, [32, 12, 20, 3, 12])
        self.assertEquals(self.pages.page(2).next_page_number(), 3)
        self.assertEquals(self.pages.page(2).start_index, 5)
        self.assertEquals(self.pages.page(7).end_index, 32)


    def test_link(self):
        self.assertEquals(self.pages.page(3).next_page.previous_page, self.pages.page(3))
        self.assertEquals(self.pages.page(5).previous_page.previous_page.previous_page.page_number, 2)