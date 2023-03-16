from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    GetTagsView,
    GetIngredientsView,
    CreateRecipeView,
)

app_name = "api"

router = DefaultRouter()

router.register("tags", GetTagsView, basename="tags")
router.register("ingredients", GetIngredientsView, basename="ingredients")
router.register("recipes", CreateRecipeView, basename="recipes")


urlpatterns = [
    path("", include(router.urls)),
]
