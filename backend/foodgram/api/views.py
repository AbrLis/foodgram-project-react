from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)

from recipes.models import (
    Tags,
    Ingredient,
    SelectedRecipes,
    ShoppingList,
    Recipes,
)


# ----------------Обработка запросов рецептов----------------
class CreateRecipeView(ModelViewSet):
    """Создание, список и получение рецепта"""

    serializer_class = RecipeSerializer
    queryset = Recipes.objects.all()

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
