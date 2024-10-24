from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=127)
    trivia = models.TextField(default=None)