from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Tags(models.Model):
    """Модель тегов"""

    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name="Название тега",
        db_index=True,
    )
    color = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        validators=[RegexValidator(r"^#[0-9A-Fa-f]+$")],
        verbose_name="Цвет тега",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name="Слаг",
        db_index=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиента"""

    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name="Название ингридиента",
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=200,
        null=False,
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ["name"]


class RecipeIngregient(models.Model):
    """Модель ингридиента для рецепта"""

    ingredient = models.OneToOneField(
        Ingredient, on_delete=models.CASCADE, primary_key=True
    )
    amount = models.PositiveIntegerField(
        null=False, verbose_name="Количество ингридиента"
    )


class Recipes(models.Model):
    """Модель рецептов"""

    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name="Название рецепта",
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    image = models.ImageField(
        upload_to="recipes/", null=False, verbose_name="Изображение рецепта"
    )
    text = models.TextField(
        max_length=200, null=False, verbose_name="Текст рецепта"
    )
    cooking_time = models.PositiveIntegerField(
        null=False, verbose_name="Время приготовления"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, null=False, verbose_name="Дата публикации"
    )
    tags = models.ManyToManyField(
        Tags,
        blank=True,
        related_name="recipes",
        verbose_name="Теги",
        db_index=True,
    )
    ingredients = models.ManyToManyField(
        RecipeIngregient,
        blank=True,
        related_name="recipes",
        verbose_name="Ингридиенты",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["name"]

    def __str__(self):
        return self.title


class SelectedRecipes(models.Model):
    """Модель избранных рецептов"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="selected_recipes",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        null=False,
        related_name="selected_recipes",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        ordering = ["user"]

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["user"]

    def __str__(self):
        return self.user.username
