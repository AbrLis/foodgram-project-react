from django.core.exceptions import ValidationError
from recipes.models import Tags


def tags_exist(tags: list[int]):
    """Проверка на существование тегов. На вход принимает список id тегов."""
    tags_check = Tags.objects.filter(pk__in=tags)
    if len(tags_check) != len(tags):
        raise ValidationError('Тег не найден')
