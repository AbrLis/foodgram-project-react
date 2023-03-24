from django.core.exceptions import ValidationError

from recipes.models import Tags


def tags_exist(tags: list[int]):
    """Проверка на существование тегов. На вход принимает список id тегов."""
    tags_check = Tags.objects.filter(pk__in=tags)
    if len(tags_check) != len(tags):
        raise ValidationError("Тег не найден")


def inrg_exist(ingredients: list[dict]):
    """
    Проверка на существование ингридиентов.
    На вход принимает список ингридиентов.
    """
    count_ingr = 0
    for ingr in ingredients:
        if ingr.get('id') and int(ingr.get('amount')) > 0:
            count_ingr += 1
    if len(ingredients) != count_ingr:
        raise ValidationError("Ошибка в данных ингридиентов")
