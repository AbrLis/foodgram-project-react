from enum import Enum


class UrlParams(str, Enum):
    # Параметр тегов
    TAGS = 'tags'
    # Параметр ингридиентов
    INGREDIENTS = 'name'
    # Параметр избранного
    FAVORITE = 'is_favorited'
    # Параметр покупок
    SHOP_CART = 'is_in_shopping_cart'
    # Параметр автора
    AUTHOR = 'author'
