from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = "admin"
USER = "user"


class User(AbstractUser):
    """Модель пользователя"""

    ROLE_CHOICES = (
        (ADMIN, "Администратор"),
        (USER, "Пользователь"),
    )

    role = models.CharField(
        verbose_name="Роль",
        max_length=30,
        choices=ROLE_CHOICES,
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Почта"
    )
    first_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Фамилия"
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser
