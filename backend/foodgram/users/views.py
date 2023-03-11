from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from djoser import utils
from djoser.conf import settings
from djoser.views import UserViewSet, TokenCreateView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer, MyUserCreateSerializer

User = get_user_model()


class UserCreateTokenViewSet(TokenCreateView):
    """Класс api/auth/token/login/ для получения токена"""

    def post(self, request, *args, **kwargs):
        """Получение токена по email и паролю"""
        username = User.objects.get(email=request.data["email"]).username
        request.data["username"] = username
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED,
        )


class UserSignUpViewSet(CreateAPIView, ListAPIView):
    """Path api/users/ для регистрации и получения списка пользователей"""

    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """Создание пользователя"""
        response = super().create(request, *args, **kwargs)
        del response.data["password"]
        return Response(response.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        """Возвращает сериализатор для списка пользователей"""
        if self.request.method == "GET":
            return UserSerializer
        return MyUserCreateSerializer


class UserChangePasswordViewSet(UserViewSet):
    """Изменение пароля пользователя"""

    @login_required
    @action(detail=False, methods=["post"])
    def set_password(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

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


class UserDetailViewSet(RetrieveAPIView):
    """Получение информации о пользователе по id"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        id_user = self.kwargs.get("id")
        if id_user == "me":
            user = self.request.user
        else:
            user = get_object_or_404(User, pk=id_user)
        return user
