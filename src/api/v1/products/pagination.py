from rest_framework.pagination import CursorPagination, PageNumberPagination


class SearchProductPagePagination(PageNumberPagination):
    page_size = 25
    page_query_param = 'page'
    max_page_size = 50
    page_size_query_param = 'page_size'


class SearchProductCursorPagination(CursorPagination):
    cursor_query_param = 'c'
    ordering = '-created_at'
    page_size = 25
    page_size_query_param = 'page_size'


class ProductReviewPagePagination(PageNumberPagination):
    page_size = 25
    page_query_param = 'page'
    max_page_size = 50
    page_size_query_param = 'page_size'
