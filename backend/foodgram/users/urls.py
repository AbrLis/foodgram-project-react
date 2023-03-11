from django.urls import path, re_path
from djoser.views import TokenDestroyView

from .views import (
    UserSignUpViewSet,
    UserDetailViewSet,
    UserChangePasswordViewSet,
    UserCreateTokenViewSet,
)

app_name = "users"

urlpatterns = [
    path(
        "users/",
        UserSignUpViewSet.as_view(),
    ),
    re_path(
        r"^users/(?P<id>(\d+|me))/$",
        UserDetailViewSet.as_view(),
        name="user_detail",
    ),
    path(
        "users/set_password/",
        UserChangePasswordViewSet.as_view({"post": "set_password"}),
        name="change_password",
    ),
    path(
        "auth/token/login/",
        UserCreateTokenViewSet.as_view(),
        name="token_create",
    ),
    path(
        "auth/token/logout/", TokenDestroyView.as_view(), name="token_destroy"
    ),
]
