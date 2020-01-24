class Page:
    
    object_list = []
    page_number = 1

    previous_page = None
    next_page = None

    start_index = 0
    end_index = 0

    def __init__(self, object_list, start_index = 0):
        self.object_list = object_list
        self.start_index = start_index
        self.end_index = self.start_index + len(object_list) - 1
        
    
    def has_next(self):
        return self.next_page is not None
    
    def has_previous(self):
        return self.previous_page is not None

    def has_other_pages(self):
        return self.has_next() or self.has_previous()
    
    def next_page_number(self):
        if self.has_next():
            return self.next_page.page_number
        else:
            raise Exception('No such page')
    
    def previous_page_number(self):
        if self.has_previous():
            return self.previous_page.page_number
        else:
            raise Exception('No such page')

    def __str__(self):
        return "Page : {}, Data: {}".format(self.page_number, str(self.object_list))
    

class Paginator:
        
    count = 0
    num_pages = 0
    first_page = None
    last_page = None
    
    def __init__(self, items, items_per_page):
        self.count = len(items)
        self.num_pages = -(-len(items) // items_per_page)
        self._populate_pages(items, items_per_page)

    def _add_page(self, object_list, start_index):
        new_page = Page(object_list, start_index)
        if self.first_page:
            self.last_page.next_page = new_page
            new_page.previous_page = self.last_page
            new_page.page_number = self.last_page.page_number + 1
            self.last_page = new_page
        else:
            self.first_page = new_page
            self.last_page = new_page
        return new_page

    def _populate_pages(self, items, items_per_page):
        start = 0
        end = start + items_per_page

        while start < self.count:
            page = self._add_page(items[start:end], start)
            start = end
            end += items_per_page
            if (end > self.count):
                end = self.count
    
    def page_range(self):
        return range(1, self.last_page.page_number + 1)

    def page(self, index):
        page = self.first_page
        while page:
            if index == page.page_number:
                return page
            page = page.next_page
        raise Exception('No such page')

        
    
    
    
    
    
    
    
    