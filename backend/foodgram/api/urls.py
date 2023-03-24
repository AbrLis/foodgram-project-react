from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateRecipeView, GetIngredientsView, GetTagsView

app_name = "api"

router_v1 = DefaultRouter()

router_v1.register("tags", GetTagsView, basename="tags")
router_v1.register("ingredients", GetIngredientsView, basename="ingredients")
router_v1.register("recipes", CreateRecipeView, basename="recipes")


urlpatterns = [
    path("", include(router_v1.urls)),
]
