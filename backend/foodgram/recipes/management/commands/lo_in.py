import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Loads ingredients from a CSV file"

    def handle(self, *args, **options):
        self.stdout.write("Loading ingredients...")
        path_to_csv = "./data/ingredients.csv"
        with open(path_to_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                Ingredient.objects.update_or_create(
                    name=row[0], measurement_unit=row[1]
                )
        self.stdout.write(
            self.style.SUCCESS("Ingredients loaded successfully")
        )
