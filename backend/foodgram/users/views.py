from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.paginators import PageLimitPagination
from users.serializers import SubscriptionSerializer
from recipes.models import Follow
from core.params import UrlParams

User = get_user_model()


class MyUserViewSet(UserViewSet):
    """Обработка запросов к модели User"""

    pagination_class = PageLimitPagination

    @action(detail=False, methods=("get",), url_path="subscriptions")
    def subscriptions(self, request, *args, **kwargs):
        """
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты ограниченные параметром recipes_limit.
        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset_user = User.objects.filter(
            id__in=Follow.objects.select_related("author").values("user")
        )
        page = self.paginate_queryset(queryset_user.order_by("id"))
        serializer = SubscriptionSerializer(page, many=True)

        return self.get_paginated_response(
            self.recipes_limit(request, serializer)
        )

    @action(
        detail=True,
        methods=("post", "delete"),
    )
    def subscribe(self, request, id, *args, **kwargs):
        """
        Подписывает или удаляет подписку на автора рецептов с ограничением
        в параметре recipes_limit.
        """
        # TODO: Похожий код в api/views.py CreateRecipeView
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        author = get_object_or_404(User, id=id)
        current_user = self.request.user

        connection = Follow.objects.filter(
            Q(author=current_user) & Q(user=author)
        )

        if (request.method in ("POST",)) and not connection:
            if author == current_user:
                return Response(
                    {"error": "You can't subscribe to yourself"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Follow(None, author.id, current_user.id).save()
            return Response(
                self.recipes_limit(request, SubscriptionSerializer(author)),
                status=status.HTTP_201_CREATED,
            )

        if (request.method in ("DELETE",)) and connection:
            connection[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def recipes_limit(self, request, serializer) -> SubscriptionSerializer:
        """Обработка параметра recipes_limit в запросе"""

        params = request.query_params.get(UrlParams.RECIPES_LIMIT.value)
        if params:
            serializer.data[0]["recipes"] = serializer.data[0]["recipes"][
                : int(params)
            ]
        return serializer.data
