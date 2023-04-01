from api.mixins import AddManyToManyFieldMixin
from api.paginators import PageLimitPagination
from core.params import SUBSCRIBED, UrlParams
from django.contrib.auth import get_user_model
from django.db.models import Q
from djoser.views import UserViewSet
from recipes.models import Follow
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import SubscriptionSerializer

User = get_user_model()


class MyUserViewSet(UserViewSet, AddManyToManyFieldMixin):
    """Обработка запросов к модели User"""

    pagination_class = PageLimitPagination
    serializers_for_mixin = SubscriptionSerializer

    def get_serializer_context(self):
        """
        Добавление в контекст списка подписок для проверки в сериализаторе,
        добавляется список id авторов, на которых подписан пользователь
        """

        context = super().get_serializer_context()
        context[SUBSCRIBED] = self.request.user.subscribers.values_list(
            "author_id", flat=True
        )
        return context

    @action(detail=False, methods=("get",), url_path="subscriptions")
    def subscriptions(self, request, *args, **kwargs):
        """
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты ограниченные параметром recipes_limit.
        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset_user = User.objects.filter(
            subscriptions__user=self.request.user
        )
        page = self.paginate_queryset(queryset_user.order_by("id"))
        serializer = SubscriptionSerializer(page, many=True)

        params = request.query_params.get(UrlParams.RECIPES_LIMIT.value)

        try:
            if params:
                serializer.data[0]["recipes"] = serializer.data[0]["recipes"][
                    : int(params)
                ]
        except IndexError:
            # Обработка случая пустого списка рецептов
            pass

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=("post", "delete"),
    )
    def subscribe(self, request, id, *args, **kwargs):
        """
        Подписывает или удаляет подписку на автора рецептов с ограничением
        в параметре recipes_limit.
        """
        request_response = self.delete_create_many_to_many(
            id, Follow, Q(author=id)
        )

        params = request.query_params.get(UrlParams.RECIPES_LIMIT.value)

        if (
            params
            and request.method == "POST"
            and request_response.status_code == 201
            and request_response.data.get("recipes")
        ):
            request_response.data["recipes"] = request_response.data[
                "recipes"
            ][: int(params)]

        return request_response
