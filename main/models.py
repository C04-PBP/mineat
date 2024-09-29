from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=127,default= "No Name")
    location = models.CharField(max_length=255,default= "Location Unknown")
    review = models.FloatField(default= 0.0)


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=127)
    price = models.PositiveIntegerField(default= 0)
    description = models.TextField(default= "")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name= "food")
    review = models.FloatField(default= 0.0)