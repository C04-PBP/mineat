from django.core.management import BaseCommand
from database_commands.management.commands.load_food import Command as LoadFood
from database_commands.management.commands.load_ingredient import Command as LoadIngredient
from database_commands.management.commands.load_district import Command as LoadDistrict
from database_commands.management.commands.load_restaurant import Command as LoadRestaurant

class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        self.stdout.write("Memuat Fnb")
        LoadFood.handle(self)
        self.stdout.write("Selesai memuat Fnb")

        self.stdout.write("Memuat Bahan")
        LoadIngredient.handle(self)
        self.stdout.write("Selesai memuat Bahan")

        self.stdout.write("Memuat Lokasi")
        LoadDistrict.handle(self)
        self.stdout.write("Selesai memuat Lokasi")

        self.stdout.write("Memuat Restaurant")
        LoadRestaurant.handle(self)
        self.stdout.write("Selesai memuat Restaurant")
