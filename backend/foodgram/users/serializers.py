from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


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
        user = self.context["request"].user
        return (
            user.is_authenticated and user.follower.filter(author=obj).exists()
        )


class MyUserChangePasswordSerializer(UserCreateSerializer):
    """Сериализатор для изменения пароля пользователя"""

    class Meta(UserCreateSerializer):
        model = User
        fields = ("password", "new_password")


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя"""

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("email", "username", "first_name", "password", "last_name")
