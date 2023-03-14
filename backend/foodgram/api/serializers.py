import base64
import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import (
    Tags,
    Ingredient,
    Recipes,
    RecipeIngregient,
    ShoppingList,
    SelectedRecipes,
)
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tags
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиента"""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиента для рецепта"""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.CharField(source="id.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="id.measurement_unit", read_only=True
    )
    amount = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""

    author = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    image = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True, min_value=1)
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True, required=True
    )

    class Meta:
        model = Recipes
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def create(self, validated_data):
        """Создает рецепт с ингридиентами, тегами и картинкой в базе данных"""

        validated_data["image"] = self.save_image(validated_data["image"])
        validated_data["author"] = self.context["request"].user

        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipes.objects.create(**validated_data)

        recipe.tags.set(tags)
        recipe.ingredients.set(self.create_ingridients(recipe, ingredients))

        return recipe

    # def is_favorited(self, obj):
    #     """Проверяет, добавлен ли рецепт в избранное"""
    #     user = self.context["request"].user
    #     return (
    #         user.is_authenticated
    #         and SelectedRecipes.objects.filter(user=user, recipe=obj).exists()
    #     )
    #
    # def is_in_shopping_cart(self, obj):
    #     """Проверяет, добавлен ли рецепт в список покупок"""
    #     user = self.context["request"].user
    #     return (
    #         user.is_authenticated
    #         and ShoppingList.objects.filter(user=user, recipe=obj).exists()
    #     )

    def create_ingridients(self, recipe, ingredients):
        """Создает ингридиенты для рецепта"""
        ingredients_list = []
        for ingredient in ingredients:
            x = RecipeIngregient.objects.create(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            )
            x.save()
            ingredients_list.append(x)
        return ingredients_list

    def save_image(self, file):
        """Сохраняет картинку в файловую систему"""
        domain = self.context["request"].get_host()
        file = self.convert_base64_to_image(file)
        default_storage.save(file.name, file)
        media_url = default_storage.url(file.name)
        return f"http://{domain}{media_url}"

    def convert_base64_to_image(self, image_data):
        """Преобразует base64 строку в объект изображения"""
        format_img, imgstr = image_data.split(";base64,")
        ext = format_img.split("/")[-1]
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        name = f"recipe_image_{time}.{ext}"
        image = ContentFile(base64.b64decode(imgstr), name=name)
        return image
