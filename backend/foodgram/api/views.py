from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TagSerializer, IngredientsListSerializer

from recipes.models import Tags, IngredientsList


# ----------------Получение ингридиентов----------------
class GetIngredientView(RetrieveAPIView):
    """Получение ингридиента по id"""

    queryset = IngredientsList.objects.all()
    serializer_class = IngredientsListSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs["id"])


class GetIngredientsView(ListAPIView):
    """Получение списка ингридиентов с возможностью поиска в начале строки"""

    queryset = IngredientsList.objects.all()
    serializer_class = IngredientsListSerializer
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["^name"]
    ordering_fields = ["name"]


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
