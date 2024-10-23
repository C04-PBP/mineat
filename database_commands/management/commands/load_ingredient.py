import csv
from django.core.management import BaseCommand
from fnb.models import Fnb
from ingredient.models import Ingredient

class Command(BaseCommand):
    help = 'Memasukkan Food ke dataset'

    def handle(self, *args,**kwargs):
        path = "ingredient_mapping.csv"

        

        try:
            with open("ingredient_mapping.csv","rt",encoding= "utf-8") as file:
                reader = csv.reader(file,dialect="excel")
                
                # Skip header 
                next(reader, None)

                for row in reader:
                    ingridient, created = Ingredient.objects.get_or_create(name = row[0])
                    # if created:
                    #     self.stdout.write(f"Successfully created Ingredient: {row[0]}")
                    # else:
                    #     self.stdout.write(f"Ingredient {row[0]} already exists.")

                    for i in row[1].strip("[").strip("]").split(","):
                        try:
                            name = i.strip().strip("'").strip('"')
                            food = Fnb.objects.get(name= name)
                            ingridient.fnb.add(food)
                        except Fnb.DoesNotExist:
                            self.stdout.write(f"Ingredient : Food with name {i} don't exist ")
                        

        except FileNotFoundError:
            self.stderr.write(f"File not found: {path}")
        except UnicodeDecodeError as e:
            self.stderr.write(f"Encoding error while reading file: {e}")
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
