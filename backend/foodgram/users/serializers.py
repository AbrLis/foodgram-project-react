from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

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
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, validators=[validate_password]
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
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
        return User.objects.create_user(**validated_data)
