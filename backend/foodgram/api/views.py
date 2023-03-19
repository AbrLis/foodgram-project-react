from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)
from .paginators import PageLimitPagination

from recipes.models import (
    Tags,
    Ingredient,
    SelectedRecipes,
    ShoppingList,
    Recipes,
)

from core.params import UrlParams


# ----------------Обработка запросов рецептов----------------
class CreateRecipeView(ModelViewSet):
    """Создание, список и получение рецепта"""

    serializer_class = RecipeSerializer
    queryset = Recipes.objects.all()
    pagination_class = PageLimitPagination

    def get_queryset(self):
        """Подготовка queryset для запросов params"""

        quryset = self.queryset
        tags = self.request.query_params.get(UrlParams.TAGS.value)
        if tags:
            quryset = quryset.filter(tags__slug__in=tags).distinct()

        author = self.request.query_params.get(UrlParams.AUTHOR.value)
        if author:
            quryset = quryset.filter(author=author)

        if self.request.user.is_anonymous:
            return quryset

        # Обработка параметров для списка покупок
        in_shop_cart = self.request.query_params.get(UrlParams.SHOP_CART.value)
        if in_shop_cart:
            quryset = quryset.filter(shoppinglist__user=self.request.user)
        elif in_shop_cart is False:
            quryset = quryset.exclude(shoppinglist__user=self.request.user)

        # Обработка параметров для избранных рецептов
        in_favorites = self.request.query_params.get(UrlParams.FAVORITE.value)
        if in_favorites:
            quryset = quryset.filter(selectedrecipes__user=self.request.user)
        elif in_favorites is False:
            quryset = quryset.exclude(selectedrecipes__user=self.request.user)

        return quryset

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthorOrReadOnly]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


# ----------------Получение ингридиентов с поиском----------------
class GetIngredientsView(ListAPIView, RetrieveAPIView, GenericViewSet):
    """Получение списка ингридиентов с возможностью поиска в начале строки"""

    queryset = Ingredient.objects.all()
    pagination_class = PageLimitPagination
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["^name"]


# ----------------Получение тегов----------------
class GetTagsView(ListAPIView, RetrieveAPIView, GenericViewSet):
    """Получение списка тегов"""

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageLimitPagination
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
