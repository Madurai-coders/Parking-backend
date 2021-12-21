from rest_framework.pagination import PageNumberPagination


class SmallSetPagination(PageNumberPagination):
    page_size = 3

class fourSetPagination(PageNumberPagination):
    page_size = 4

class tenSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size' 
    max_page_size = 200
    last_page_strings = ('the_end',)
