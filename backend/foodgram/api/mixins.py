from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class AddManyToManyFieldMixin:
    """Добавление, удаление данных ManyToManyField для моделей"""

    serializers_for_mixin = None

    def delete_create_many_to_many(
        self, object_idx, model_object, filters_object
    ):
        object_data = get_object_or_404(self.queryset, id=object_idx)
        connections = model_object.objects.filter(
            Q(user=self.request.user) & filters_object
        )
        serializer = self.serializers_for_mixin(object_data)

        if (self.request.method in ("POST", "GET")) and not connections:
            model_object(None, object_data.id, self.request.user.id).save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if (self.request.method in ("DELETE",)) and connections:
            connections[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": "object exist"}, status=status.HTTP_400_BAD_REQUEST
        )
