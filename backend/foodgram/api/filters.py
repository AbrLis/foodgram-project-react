import django_filters.rest_framework as filters
from core.params import UrlParams
from recipes.models import Ingredient, Recipes


# ----------------Поисковой фильтр ингридиентов----------------
class IngredientsFilter(filters.FilterSet):
    """Фильтр для ингридиентов"""

    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


# ----------------Фильтр класс для рецептов----------------
class RcipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name="tags__slug", distinct=True)
    author = filters.CharFilter(field_name="author", lookup_expr="exact")
    is_in_shopping_cart = filters.CharFilter(
        method="filter_by_boolean", field_name="in_shopping_list__user"
    )
    is_favorited = filters.CharFilter(
        method="filter_by_boolean", field_name="selected_recipes__user"
    )

    class Meta:
        model = Recipes
        fields = ("tags", "author", "is_in_shopping_cart", "is_favorited")

    def filter_by_boolean(self, queryset, name, value):
        if value == UrlParams.IS_TRUE.value:
            return queryset.filter(**{name: self.request.user})
        if value == UrlParams.IS_FALSE.value:
            return queryset.exclude(**{name: self.request.user})
        return queryset
