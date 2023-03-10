from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import MyUserCreateSerializer, UserSerializer

User = get_user_model()


class UserSignUpViewSet(UserViewSet):
    """Класс api/users/ для регистрации и получения списка пользователей"""

    # @action(detail=False, methods=["post"])
    def create(self, request, *args, **kwargs):
        """Регистрация пользователя"""
        serializer = MyUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )

    @login_required
    @action(detail=False, methods=["get"])
    def list(self, request, *args, **kwargs):
        """Получение списка всех пользователей"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordViewSet(UserViewSet):
    """Изменение пароля пользователя"""

    @login_required
    @action(detail=False, methods=["post"])
    def set_password(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data["new_password"]
            curent_password = serializer.validated_data["current_password"]

            if not user.check_password(curent_password):
                return Response(
                    {"current_password": "Wrong password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()
            return Response(
                {"status": "password set"}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailViewSet(UserViewSet):
    """Получение информации о пользователе по id"""

    @login_required
    @action(detail=False, methods=["get"])
    def get_user(self, request, *args, **kwargs):
        id_user = kwargs.get("id")
        if id_user == "me":
            user = request.user
        else:
            user = User.objects.get(pk=id_user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
