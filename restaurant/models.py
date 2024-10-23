from django.db import models
from django.contrib.auth.models import User
import uuid
from location.models import Location
from fnb.models import Fnb

# Create your models here.
class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=127)
    address = models.TextField()
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    fnb = models.ManyToManyField(Fnb,related_name= "restaurant_fnb")
