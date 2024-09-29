import csv
from django.core.management import BaseCommand
from main.models import Food,Restaurant

class Command(BaseCommand):
    help = 'Memasukkan Food ke dataset'

    def handle(self, default_user):
        path = "indian_food.csv"

        restaurants = Restaurant.objects.all()  


        try:
            with open(path, 'rt', encoding='utf-8') as file:  
                reader = csv.reader(file, dialect='excel')

                # Buat ngelompokin makanan ke restoran
                restaurant_index = 0

                # Skip header 
                next(reader, None)

                for i,row in enumerate(reader):
                    try:
                        
                        # Pake get or create biar gada duplicate
                        _, created = Food.objects.get_or_create(
                            user = default_user,
                            name = row[0],
                            price = 0,
                            description = f"rasa = {row[5]}, jenis = {row[6]}, asal = {row[7]}",
                            restaurant = restaurants[restaurant_index],
                            review = 0,
                            
                        )
                        if created:
                            self.stdout.write(f"Successfully created Food: {row[0]}")
                        else:
                            self.stdout.write(f"Food {row[0]} already exists.")

                    except Exception as e:
                        self.stderr.write(f"Error creating Food from row {row}: {e}")
                
                    # Logikanya kalo total food ada 254 jadi dibagi ke 64 makanya 4 baru pindah resto
                    if i % 4 == 0 and i != 0:
                        restaurant_index += 1


        except FileNotFoundError:
            self.stderr.write(f"File not found: {path}")
        except UnicodeDecodeError as e:
            self.stderr.write(f"Encoding error while reading file: {e}")
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
