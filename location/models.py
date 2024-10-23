from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=127)
    