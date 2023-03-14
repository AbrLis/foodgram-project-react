from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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



# ----------------Получение ингридиентов----------------
class GetIngredientView(RetrieveAPIView):
    """Получение ингридиента по id"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs["id"])


# ----------------Получение ингридиентов с поиском----------------
class GetIngredientsView(ListAPIView):
    """Получение списка ингридиентов с возможностью поиска в начале строки"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["^name"]


# ----------------Получение тегов----------------
class GetTagView(RetrieveAPIView):
    """Получение тега по id"""

    queryset = Tags.objects.all()
    serializer_class = TagSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs["id"])


class GetTagsView(ListAPIView):
    """Получение списка тегов"""

    queryset = Tags.objects.all()
    serializer_class = TagSerializer
