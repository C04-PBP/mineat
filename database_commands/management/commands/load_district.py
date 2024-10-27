import csv
from django.core.management import BaseCommand
from location.models import Location


class Command(BaseCommand):
    help = 'Memasukkan Food ke dataset'

    def handle(self,*args,**kwargs):
        path = "district.csv"
        

        try:
            with open(path, 'rt', encoding='utf-8') as file:  
                reader = csv.reader(file, dialect='excel',delimiter=",")


                # Skip header 
                next(reader, None)

                for row in reader:
                    try:
                        
                        # Pake get or create biar gada duplicate
                        _, created = Location.objects.get_or_create(
                            name = row[0].strip(" "),
                            trivia = row[1].strip(" "),
                            image = row[2].strip(" ")
                            
                        )
                        if created:
                            self.stdout.write(f"Successfully created Location: {row[0]}")
                        else:
                            self.stdout.write(f"Location {row[0]} already exists.")

                    except Exception as e:
                        self.stderr.write(f"Error creating Food from row {row}: {e}")
                
                    
        except FileNotFoundError:
            self.stderr.write(f"File not found: {path}")
        except UnicodeDecodeError as e:
            self.stderr.write(f"Encoding error while reading file: {e}")
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
