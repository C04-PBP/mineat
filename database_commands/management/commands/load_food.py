import csv
from django.core.management import BaseCommand
from fnb.models import Fnb
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Memasukkan Food ke dataset'

    def handle(self,*args,**kwargs):
        path = "fnb3.csv"
        default_user,_ = User.objects.get_or_create(
                    username="bang etmin",
                    defaults={
                        "password": "something-something"  
                    }
                )

        try:
            with open(path, 'rt', encoding='utf-8') as file:  
                reader = csv.reader(file, dialect='excel',delimiter=";")


                # Skip header 
                next(reader, None)

                for row in reader:
                    try:
                        
                        # Pake get or create biar gada duplicate
                        _, created = Fnb.objects.get_or_create(
                            user = default_user,
                            name = row[0].strip(" "),
                            price = row[1],
                            description = row[2],
                            # image = row[3]
                        )
                        if created:
                            self.stdout.write(f"Successfully created Food: {row[0]}")
                        else:
                            self.stdout.write(f"Food {row[0]} already exists.")

                    except Exception as e:
                        self.stderr.write(f"Error creating Food from row {row}: {e}")
                
                    
        except FileNotFoundError:
            self.stderr.write(f"File not found: {path}")
        except UnicodeDecodeError as e:
            self.stderr.write(f"Encoding error while reading file: {e}")
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
