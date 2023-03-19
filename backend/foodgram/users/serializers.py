from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipes

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о пользователе"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        return (
            obj.is_authenticated
            and obj.subscribers.filter(author=obj).exists()
        )


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя"""

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, validators=[validate_password], write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )

    def validate(self, attrs):
        email = User.objects.filter(email=attrs["email"])
        if email:
            raise serializers.ValidationError("Email already exists")
        username = User.objects.filter(username=attrs["username"])
        if username:
            raise serializers.ValidationError("Username already exists")
        return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        validated_data.pop("password")
        return user


class SubcriptionRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов в подписках"""

    class Meta:
        model = Recipes
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
        read_only_fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для подписок"""

    recipes_count = serializers.SerializerMethodField()
    recipes = SubcriptionRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()
