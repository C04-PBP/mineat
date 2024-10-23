import pandas as pd
import csv


df = pd.read_csv("fnb3.csv",sep=";")

tex = pd.read_csv("ingredients.csv",sep=";")


# try:
#     with open("fnb3.csv","rt",encoding= "utf-8") as file:
#         reader = csv.reader(file,dialect="excel",delimiter= ";")
#         for i,row in enumerate(reader):
#             print(row[0])

# except FileNotFoundError:
#     print("gagal")

to_be_set = tex.ingredient

lst = []

for i in range(len(to_be_set)):
    lst += to_be_set[i].split(",")

set_akhir = set(lst)

set_akhir.discard("")

dict_ingredient = dict()


for i in set_akhir:
    lst = []

    for num,j in enumerate(tex.ingredient):
        
        if i in j:
            lst.append(tex.iloc[num,0])
            
    dict_ingredient[i] = lst

ingredient_df = pd.DataFrame(list(dict_ingredient.items()), columns=['Ingredient', 'Foods'])

import os

# Read random bytes from os.urandom, then convert to integer
random_bytes = os.urandom(1)  # 4 bytes for a 32-bit integer
random_number = int.from_bytes(random_bytes, 'big') % 11  # % 101 to get a number between 0 and 100

print(random_number)


# print(ingredient_df.head())

# ingredient_df.to_csv("ingredient_mapping.csv", index=False)

# try:
#     with open("ingredient_mapping.csv","rt",encoding= "utf-8") as file:
#         reader = csv.reader(file,dialect="excel")
#         for row in reader:
#             ingridient, created = Ingridient.get_or_create(name = row[0])
#             for i in row[1].split(","):
#                 food = Food.object.filter(name= i)
#                 ingridient.add(food)

# except FileNotFoundError:
#     print("gagal")