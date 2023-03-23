from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyUserViewSet

app_name = "users"

router = DefaultRouter()
router.register("users", MyUserViewSet, basename="users")

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),

    # Перенаправлять остальные запросы в приложение api
    path("", include("api.urls")),
]
