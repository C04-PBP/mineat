from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Fnb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    image = models.ImageField()
    price = models.PositiveIntegerField()
    description = models.TextField()
    ingredients = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name