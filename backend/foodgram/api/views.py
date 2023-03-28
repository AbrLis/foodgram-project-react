import django_filters.rest_framework as filters

from django.db.models import F, Q, Sum
from django.http import HttpResponse
from recipes.models import (Ingredient, Recipes, SelectedRecipes, ShoppingList,
                            Tags)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RcipeFilter

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


# ----------------Поисковой фильтр ингридиентов----------------
class IngredientsFilter(filters.FilterSet):
    """Фильтр для ингридиентов"""

    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


# ----------------Получение ингридиентов с поиском----------------
class GetIngredientsView(ListAPIView, RetrieveAPIView, GenericViewSet):
    """Получение списка ингридиентов с возможностью поиска в начале строки"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientsFilter


# ----------------Получение тегов----------------
class GetTagsView(ListAPIView, RetrieveAPIView, GenericViewSet):
    """Получение списка тегов"""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
