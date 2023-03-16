from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from api.paginators import PageLimitPagination

User = get_user_model()


class MyUserViewSet(UserViewSet):
    """Обработка запросов к модели User"""

    pagination_class = PageLimitPagination
