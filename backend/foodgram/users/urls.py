from django.urls import path, re_path
from djoser.views import TokenCreateView, TokenDestroyView

from .views import (
    UserSignUpViewSet,
    UserDetailViewSet,
    UserChangePasswordViewSet,
)

app_name = "users"

urlpatterns = [
    path(
        "users/",
        UserSignUpViewSet.as_view({"post": "create", "get": "list"}),
    ),
    re_path(
        r"^users/(?P<id>(\d+|me))/$",
        UserDetailViewSet.as_view({"get": "get_user"}),
    ),
    path(
        "users/set_password/",
        UserChangePasswordViewSet.as_view({"post": "set_password"}),
    ),
    path("auth/token/login/", TokenCreateView.as_view(), name="token_create"),
    path(
        "auth/token/logout/", TokenDestroyView.as_view(), name="token_destroy"
    ),
]
