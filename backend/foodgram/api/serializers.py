from rest_framework import serializers

from recipes.models import Tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name", "color", "slug")
