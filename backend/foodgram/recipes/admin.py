from django.contrib import admin

from .models import Ingrigients, Recipes, Tags, SelectedRecipes


class IngrigientsAdmin(admin.ModelAdmin):
    """Админка ингридиентов"""

    list_display = (
        "title",
        "dimension",
    )
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"
    sortable_by = ("title",)


class TagsAdmin(admin.ModelAdmin):
    """Админка тегов"""

    list_display = ("title", "color", "slug")
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"
    sortable_by = ("title",)


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


admin.site.register(Ingrigients, IngrigientsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Recipes, RecipeAdmin)
admin.site.register(SelectedRecipes, SelectedRecipesAdmin)
