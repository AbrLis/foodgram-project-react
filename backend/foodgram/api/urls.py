from django.urls import path

from .views import (
    GetTagView,
    GetTagsView,
    GetIngredientView,
    GetIngredientsView,
)

app_name = "api"

urlpatterns = [
    path("tags/", GetTagsView.as_view(), name="tags"),
    path("tags/<int:id>/", GetTagView.as_view(), name="tag"),
    path("ingredients/", GetIngredientsView.as_view(), name="ingredients"),
    path(
        "ingredients/<int:id>/", GetIngredientView.as_view(), name="ingredient"
    ),
]
