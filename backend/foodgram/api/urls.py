from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateRecipeView, GetIngredientsView, GetTagsView

app_name = "api"

router = DefaultRouter()

router.register("tags", GetTagsView, basename="tags")
router.register("ingredients", GetIngredientsView, basename="ingredients")
router.register("recipes", CreateRecipeView, basename="recipes")


urlpatterns = [
    path("", include(router.urls)),
]
