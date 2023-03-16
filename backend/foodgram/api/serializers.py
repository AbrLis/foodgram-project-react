import base64
import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import F
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

from core import validators


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tags
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиента"""

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""

    author = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    image = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True, min_value=1)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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
            "is_favorited",
            "is_in_shopping_cart",
        )

    def create(self, validated_data):
        """Создает рецепт с ингридиентами, тегами и картинкой в базе данных"""

        validated_data["image"] = self.save_image(validated_data["image"])

        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipes.objects.create(**validated_data)

        recipe.tags.set(tags)
        self.create_ingridients(recipe, ingredients)

        return recipe

    def validate(self, data):
        """
        Проверяет, что ингридиенты и теги указаны
        и дополняет информацию об авторе
        """

        tags = self.initial_data.get("tags")
        ingredients = self.initial_data.get("ingredients")

        if not tags:
            raise serializers.ValidationError("Необходимо указать теги")
        validators.tags_exist(tags)

        if not ingredients:
            raise serializers.ValidationError("Необходимо указать ингридиенты")

        data.update(
            {
                "tags": tags,
                "ingredients": ingredients,
                "author": self.context.get("request").user,
            }
        )
        return data

    def get_ingredients(self, recipes):
        """Формирует список ингридиентов для рецепта"""

        ingredients = recipes.ingredients.values(
            "id",
            "name",
            "measurement_unit",
            amount=F("recipeingregient__amount"),
        )
        return ingredients

    def get_is_favorited(self, obj):
        """Проверяет, добавлен ли рецепт в избранное"""
        user = self.context["request"].user
        return (
            user.is_authenticated
            and SelectedRecipes.objects.filter(user=user, recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Проверяет, добавлен ли рецепт в список покупок"""
        user = self.context["request"].user
        return (
            user.is_authenticated
            and ShoppingList.objects.filter(user=user, recipe=obj).exists()
        )

    def create_ingridients(self, recipe, ingredients):
        """Заполняет таблицу ингридиентов для рецепта"""
        for ingredient in ingredients:
            RecipeIngregient.objects.get_or_create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient["id"]),
                amount=ingredient["amount"],
            )

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
