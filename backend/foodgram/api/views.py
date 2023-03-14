from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)

from recipes.models import Tags, Ingredient, SelectedRecipes, ShoppingList


# ----------------Обработка запросов рецептов----------------
class CreateRecipeView(CreateAPIView):
    """Создание рецепта"""

    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]


# ----------------Получение ингридиентов с поиском----------------
class GetIngredientsView(ListAPIView, RetrieveAPIView, GenericViewSet):
    """Получение списка ингридиентов с возможностью поиска в начале строки"""

    queryset = Ingredient.objects.all()
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
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
