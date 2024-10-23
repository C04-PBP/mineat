import csv
from django.core.management import BaseCommand
from location.models import Location
from restaurant.models import Restaurant
from fnb.models import Fnb
import os

class Command(BaseCommand):
    help = 'Memasukkan Restaurant ke dataset'

    def handle(self,*args,**kwargs):
        path = "restaurants.csv"
        
        locations = Location.objects.all()
        location_index = 0
        fnb = Fnb.objects.all()
        counter = 0

        try:
            with open(path, 'rt', encoding='utf-8') as file:  
                reader = csv.reader(file, dialect='excel')



                # Skip header 
                next(reader, None)

                for i,row in enumerate(reader):
                    counter += 1
                    try:
                        
                        # Pake get or create biar gada duplicate
                        restaurant, created = Restaurant.objects.get_or_create(
                            name = row[0].strip(" "),
                            address = row[1].strip(" "),
                            location = locations[location_index]
                        )
                        if created:
                            self.stdout.write(f"Successfully created Restaurant: {row[0]}")
                            random_num_of_food = int.from_bytes(os.urandom(1), 'big') % 11  # % 11 to get a number between 0 and 10

                            for i in range(random_num_of_food):
                                random_food_num = int.from_bytes(os.urandom(1), 'big') % 93  # % 101 to get a number between 0 and 100
                                restaurant.fnb.add(fnb[random_food_num%len(fnb)])
                        else:
                            self.stdout.write(f"Restaurant {row[0]} already exists.")
                        
                        if counter ==  2:
                            location_index += 1
                            counter = 0


                    except Exception as e:
                        self.stderr.write(f"Error creating Restaurant from row {row}: {e}")
                    
                
                         
        except FileNotFoundError:
            self.stderr.write(f"File not found: {path}")
        except UnicodeDecodeError as e:
            self.stderr.write(f"Encoding error while reading file: {e}")
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
