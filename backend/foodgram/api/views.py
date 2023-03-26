from django.db.models import F, Q, Sum
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.params import UrlParams
from recipes.models import (Ingredient, Recipes, SelectedRecipes, ShoppingList,
                            Tags)

from .mixins import AddManyToManyFieldMixin
from .paginators import PageLimitPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeShortSerializer, TagSerializer)


# ----------------Обработка запросов рецептов----------------
class CreateRecipeView(ModelViewSet, AddManyToManyFieldMixin):
    """Создание, список и получение рецепта"""

    serializer_class = RecipeSerializer
    queryset = Recipes.objects.all()
    pagination_class = PageLimitPagination
    serializers_for_mixin = RecipeShortSerializer

    def get_queryset(self):
        """Подготовка queryset для запросов params"""

        # Обработка параметров для поиска по тегам и автору
        tags = self.request.query_params.getlist(UrlParams.TAGS.value)
        author = self.request.query_params.get(UrlParams.AUTHOR.value)

        tag_filter = Q()
        if tags:
            tag_filter = Q(tags__slug__in=tags)
        author_filter = Q()
        if author:
            author_filter = Q(author=author)

        quryset = self.queryset.filter(tag_filter, author_filter).distinct()

        # Обработка параметров для списка покупок и избранных
        in_shop_cart = self.request.query_params.get(UrlParams.SHOP_CART.value)
        in_favorites = self.request.query_params.get(UrlParams.FAVORITE.value)

        return quryset.filter(
            Q(in_shopping_list__user=self.request.user)
            if in_shop_cart == UrlParams.IS_TRUE.value
            else ~Q(in_shopping_list__user=self.request.user),

            Q(selected_recipes__user=self.request.user)
            if in_favorites == UrlParams.IS_TRUE.value
            else ~Q(selected_recipes__user=self.request.user),
        )

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    @action(
        methods=("GET", "POST", "DELETE"),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        """Добавление, удаление, рецепта в список избранных"""

        return self.delete_create_many_to_many(
            pk, SelectedRecipes, Q(recipe=pk)
        )

    @action(
        methods=("GET", "POST", "DELETE"),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        """Добавление, удаление, выдача рецепта в список покупок"""

        return self.delete_create_many_to_many(
            pk, ShoppingList, Q(recipe__id=pk)
        )

    @action(
        methods=("GET",), detail=False, permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Отдача пользователю списка покупок"""

        user = self.request.user
        if not user.shopping_list.exists():
            return Response(
                {"message": "Список покупок пуст"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_name = f"shopping_list_{user.username}.txt"
        shopping_list = [f"Покупки пользователя {user.username}:\n\n"]

        # Объединия ингридиенты с одинаковым названием и единицей измерения
        ingredients = (
            Ingredient.objects.filter(recipes__in_shopping_list__user=user)
            .values("name", measurement=F("measurement_unit"))
            .annotate(amount=Sum("recipeingregient__amount"))
        )

        for ingredient in ingredients:
            shopping_list.append(
                f'{ingredient["name"]} {ingredient["amount"]}'
                f' - ({ingredient["measurement"]}); \n'
            )

        response = HttpResponse(
            shopping_list, content_type="text/plain", charset="utf-8"
        )
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response


# ----------------Получение ингридиентов с поиском----------------
class GetIngredientsView(ListAPIView, RetrieveAPIView, GenericViewSet):
    """Получение списка ингридиентов с возможностью поиска в начале строки"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        """Подготовка queryset для запросов params"""

        search = self.request.query_params.get(UrlParams.NAME.value)
        if search:
            return self.queryset.filter(name__istartswith=search)
        return self.queryset


# ----------------Получение тегов----------------
class GetTagsView(ListAPIView, RetrieveAPIView, GenericViewSet):
    """Получение списка тегов"""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
