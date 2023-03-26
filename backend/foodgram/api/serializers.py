from pathlib import Path

from core import validators
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Ingredient, RecipeIngregient, Recipes,
                            SelectedRecipes, ShoppingList, Tags)
from rest_framework import serializers
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
        fields = "__all__"


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого отображения рецепта"""

    class Meta:
        model = Recipes
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("__all__",)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""

    author = UserSerializer(read_only=True)
    image = Base64ImageField()
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

        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipes.objects.create(**validated_data)

        recipe.tags.set(tags)
        self.create_ingridients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        """
        Обновляет рецепт с ингридиентами, тегами и картинкой в базе данных
        """
        if "image" in validated_data:
            # Удаляем старую картинку
            image = Path(instance.image.path)
            image.unlink()

        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        if ingredients:
            instance.ingredients.clear()
            self.create_ingridients(instance, ingredients)
        if tags:
            instance.tags.clear()
            instance.tags.set(tags)

        instance.save()
        return instance

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

        validators.inrg_exist(ingredients)
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

        return recipes.ingredients.values(
            "id",
            "name",
            "measurement_unit",
            amount=F("recipeingregient__amount"),
        )

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
