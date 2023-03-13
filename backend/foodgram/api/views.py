from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView

from .serializers import TagSerializer

from recipes.models import Tags


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

