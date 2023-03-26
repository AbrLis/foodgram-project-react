from pathlib import Path

from django.db.models.signals import post_delete
from django.dispatch import receiver
from recipes.models import Recipes


@receiver(post_delete, sender=Recipes)
def delete_old_image(sender, instance, **kwargs):
    """Удаление файла изображения при удалении рецепта"""

    image_path = Path(instance.image.path)
    if image_path.exists():
        image_path.unlink()
