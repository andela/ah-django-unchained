from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    # This indicate the page size, it overrides PAGE_SIZE .
    page_size = 10
    page_size_query_param = 'page_size'

    # This indicates the maximum  allowable requested page size.
    max_page_size = 100

