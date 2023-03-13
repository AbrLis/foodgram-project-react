from rest_framework import serializers

from recipes.models import Tags, IngredientsList


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tags
        fields = ("id", "name", "color", "slug")


class IngredientsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка ингридиентов"""

    class Meta:
        model = IngredientsList
        fields = ("id", "name", "measurement_unit")
