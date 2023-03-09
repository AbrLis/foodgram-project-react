import csv

from recipes.models import IngredientsList

path_to_csv = "../../data/ingredients.csv"


def load_data():
    """Загрузка данных из csv файла в БД IngredientsList"""

    with open(path_to_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            IngredientsList.objects.update_or_create(
                name=row[0], measurement_unit=row[1]
            )


load_data()
