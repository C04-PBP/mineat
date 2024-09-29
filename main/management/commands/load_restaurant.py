import csv
from django.core.management import BaseCommand
from main.models import Restaurant

class Command(BaseCommand):
    help = 'Memasukkan Food ke dataset'

    def handle(self, default_user):
        path = "restaurants.csv"


        try:
            with open(path, 'rt', encoding='utf-8') as file:  
                reader = csv.reader(file, dialect='excel')

                # Skip header row if necessary
                next(reader, None)

                for i,row in enumerate(reader):

                    # Buat nyetop diset ada 64 biar pas sama jumlah food (254)
                    if i > 63:
                        break

                    try:
                        
                        # Pake get or create biar gada duplicate
                        _, created = Restaurant.objects.get_or_create(
                            user = default_user,
                            name = row[0],
                            location = row[1],
                            review = row[5],
                            
                        )
                        if created:
                            self.stdout.write(f"Successfully created Restaurant: {row[0]}")
                        else:
                            self.stdout.write(f"Restaurant {row[0]} already exists.")

                    except Exception as e:
                        self.stderr.write(f"Error creating Restaurant from row {row}: {e}")


        except FileNotFoundError:
            self.stderr.write(f"File not found: {path}")
        except UnicodeDecodeError as e:
            self.stderr.write(f"Encoding error while reading file: {e}")
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
