import base64
import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers

from recipes.models import Tags, Ingredient, Recipes
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tags
        fields = ("id", "name", "color", "slug")


class IngredientsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка ингридиентов"""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов"""

    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), required=True
    )
    amount = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        model = Ingredient
        fields = ("id", "amount")

    def to_representation(self, instance):
        return IngredientsListSerializer(instance).data


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""

    name = serializers.CharField(max_length=200, required=True)
    author = serializers.SerializerMethodField()
    image = serializers.ImageField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True, min_value=1)
    ingredients = IngredientsSerializer(many=True, required=True)
    tags = TagSerializer(many=True, required=True)

    class Meta:
        model = Recipes
        fields = (
            "id",
            "name",
            "author",
            "image",
            "text",
            "cooking_time",
            "ingredients",
            "tags",
        )

    def get_author(self, obj):
        user = self.context["request"].user
        return UserSerializer(user).data

    def create(self, validated_data):
        # Сохраняем картинку в файловую систему при создании рецепта
        image_bytes = base64.b64decode(validated_data["image"])
        file_name = f'{validated_data["name"]}{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
        file = ContentFile(image_bytes)
        file_path = default_storage.save(file_name, file)
        validated_data["image"] = file_path
        return Recipes.objects.create(**validated_data)
