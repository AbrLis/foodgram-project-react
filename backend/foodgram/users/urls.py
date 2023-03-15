from django.urls import path, re_path, include

from .views import (
    UserSignUpViewSet,
    UserDetailViewSet,
    UserChangePasswordViewSet,
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
    path("auth/", include("djoser.urls.authtoken")),

    # Перенаправлять остальные запросы в приложение api
    path("", include("api.urls")),
]
