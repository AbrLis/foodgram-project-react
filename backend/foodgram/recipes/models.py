from django.contrib.auth import get_user_model
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)
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

    def __str__(self):
        return self.name


class RecipeIngregient(models.Model):
    """Модель ингридиента для рецепта"""

    recipe = models.ForeignKey(
        "Recipes",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="recipe_ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество ингридиента",
        default=1,
        validators=(
            MinValueValidator(
                1, message="Количество ингридиента не может быть меньше 1"
            ),
            MaxValueValidator(
                1000,
                message="Количество ингридиента не может быть больше 1000",
            ),
        ),
    )

    class Meta:
        verbose_name = "Ингридиент для рецепта"
        verbose_name_plural = "Ингридиенты для рецепта"
        ordering = ["recipe"]

    def __str__(self):
        return (
            f"{self.ingredient} - в количестве {self.amount} "
            f"{self.ingredient.measurement_unit}"
        )


class Recipes(models.Model):
    """Модель рецептов"""

    name = models.CharField(
        max_length=200,
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
        Ingredient,
        through="RecipeIngregient",
        related_name="recipes",
        verbose_name="Ингридиенты",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["name"]
        constraints = (
            models.UniqueConstraint(
                fields=["name", "author"],
                name="unique_recipe_for_author",
            ),
        )

    def __str__(self):
        return self.name


class SelectedRecipes(models.Model):
    """Модель избранных рецептов"""

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        null=False,
        related_name="selected_recipes",
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="selected_recipes",
        verbose_name="Пользователь",
    )


    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        ordering = ["user"]

    def __str__(self):
        return f"Пользователь {self.user.username} - {self.recipe.name}"


class Follow(models.Model):
    """Модель подписок"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="subscriptions",
        verbose_name="На кого подписан",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="subscribers",
        verbose_name="Кто подписан",
    )


    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["user"]
        constraints = (
            models.UniqueConstraint(
                fields=("author", "user"),
                name="Можно подписаться лишь один раз на одного автора",
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")),
                name="Нельзя подписаться на себя",
            ),
        )

    def __str__(self):
        return (
            f"Пользователь {self.user.username}"
            f" подписан на {self.author.username}"
        )


class ShoppingList(models.Model):
    """Модель списка покупок"""

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        null=False,
        related_name="in_shopping_list",
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="shopping_list",
        verbose_name="Пользователь",
    )


    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ["user"]

    def __str__(self):
        return (
            f"Пользователь {self.user.username}"
            f"хочет купить {self.recipe.name}"
        )
