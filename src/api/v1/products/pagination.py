from rest_framework.pagination import PageNumberPagination


class SearchProductPagination(PageNumberPagination):
    page_size = 25
    page_query_param = 'page'
    max_page_size = 50
    page_size_query_param = 'page_size'


class ProductReviewPagination(PageNumberPagination):
    page_size = 25
    page_query_param = 'page'
    max_page_size = 50
    page_size_query_param = 'page_size'
