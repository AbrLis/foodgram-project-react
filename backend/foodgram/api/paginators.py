from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Пагинатор с определением атрибута"""
    page_size_query_param = 'limit'
