from django.contrib import admin

from .models import (
    IngredientsList,
    Recipes,
    Tags,
    SelectedRecipes,
)


class TagsAdmin(admin.ModelAdmin):
    """Админка тегов"""

    list_display = ("name", "color", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    sortable_by = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов"""

    list_display = (
        "title",
        "author",
    )
    search_fields = ("title", "author")
    list_filter = ("title",)
    empty_value_display = "-пусто-"
    sortable_by = (
        "title",
        "author",
        "tags"
    )


class SelectedRecipesAdmin(admin.ModelAdmin):
    """Админка избранных рецептов"""

    list_display = (
        "user",
        "recipe",
    )
    search_fields = ("user", "recipe")
    list_filter = ("user",)
    empty_value_display = "-пусто-"
    sortable_by = (
        "user",
        "recipe",
    )


class IngridientsListAdmin(admin.ModelAdmin):
    """Админка ингридиентов"""

    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    sortable_by = (
        "name",
    )


admin.site.register(Tags, TagsAdmin)
admin.site.register(Recipes, RecipeAdmin)
admin.site.register(SelectedRecipes, SelectedRecipesAdmin)
admin.site.register(IngredientsList, IngridientsListAdmin)
