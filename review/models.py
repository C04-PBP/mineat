from django.db import models
from django.contrib.auth.models import User
from fnb.models import Fnb
import uuid
# Create your models here.
class Review(models.Model):
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    fnb = models.ForeignKey(Fnb,on_delete= models.CASCADE, related_name= "review_fnb")
