from django.db import models
from django.contrib.auth.models import User
from fnb.models import Fnb
import uuid
# Create your models here.
class Review(models.Model):
    makanan = models.ForeignKey(Fnb, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField(default=0)
    like =  models.IntegerField(default=0)
