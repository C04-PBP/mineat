from django.core.management import BaseCommand
from django.contrib.auth.models import User
from main.management.commands.load_food import Command as LoadFoodCommand
from main.management.commands.load_restaurant import Command as LoadRestaurantCommand

class Command(BaseCommand):
    help = 'Load both restaurants and food data'

    def handle(self, *args, **kwargs):
        default_user,_ = User.objects.get_or_create(
                    username="bang etmin",
                    defaults={
                        "password": "something-something"  
                    }
                )
        # Step 1: Run the load_restaurant command
        self.stdout.write("Starting to load restaurants...")
        restaurant_loader = LoadRestaurantCommand()
        restaurant_loader.handle(default_user)

        # Step 2: Run the load_food command
        self.stdout.write("Starting to load food data...")
        food_loader = LoadFoodCommand()
        food_loader.handle(default_user)

        self.stdout.write("Successfully loaded restaurants and food data.")