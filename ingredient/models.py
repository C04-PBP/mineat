from django.db import models
from django.contrib.auth.models import User
import uuid
from fnb.models import Fnb

# Create your models here.
class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=127)
    fnb = models.ManyToManyField(to= Fnb,related_name= "fnb")
