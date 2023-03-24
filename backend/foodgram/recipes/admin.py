from django.contrib import admin

from .models import (Follow, Ingredient, RecipeIngregient, Recipes,
                     SelectedRecipes, ShoppingList, Tags)


class FollowAdmin(admin.ModelAdmin):
    """Админка подписок"""

    list_display = (
        "id",
        "user",
        "author",
    )
    search_fields = (
        "user",
        "author",
    )
    list_filter = ("author",)
    empty_value_display = "-пусто-"
    sortable_by = (
        "user",
        "author",
        "id",
    )


class IngredientInline(admin.TabularInline):
    """Инлайн ингредиентов"""

    model = RecipeIngregient
    extra = 0


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
        "id",
        "name",
        "author",
        "get_count_selected_recipes",
    )
    fields = (
        ("name", "cooking_time"),
        ("author", "tags"),
        ("text",),
    )

    raw_id_fields = ("author",)
    search_fields = (
        "name",
        "author__username",
        "tags__name",
    )
    list_filter = (
        "name",
        "author__username",
        "tags__name",
    )
    inlines = (IngredientInline,)
    sortable_by = (
        "id",  # идентификатор рецепта
        "name",  # название рецепта
        "author",  # автор рецепта
        "tags",  # теги рецепта
    )

    empty_value_display = "-пусто-"

    def get_count_selected_recipes(self, obj):
        """
        Возвращает количество пользователей, добавивших рецепт в избранное
        """
        return SelectedRecipes.objects.filter(recipe=obj).count()

    get_count_selected_recipes.short_description = (
        "В избранном у пользователей"
    )


class SelectedRecipesAdmin(admin.ModelAdmin):
    """Админка списка покупок"""

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
    sortable_by = ("name",)


class ShoppingListAdmin(admin.ModelAdmin):
    """Админка списка покупок"""

    list_display = (
        "user",
        "recipe",
    )
    search_fields = ("user", "recipe")
    list_filter = ("user",)
    empty_value_display = "-пусто-"
    sortable_by = ("user", "recipe")


admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Recipes, RecipeAdmin)
admin.site.register(SelectedRecipes, SelectedRecipesAdmin)
admin.site.register(Ingredient, IngridientsListAdmin)
admin.site.register(Follow, FollowAdmin)
