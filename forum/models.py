from django.db import models
from fnb.models import Fnb
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Forum(models.Model):
    name = models.CharField(max_length= 255)
    text = models.TextField()
    # user = models.ForeignKey(User,on_delete= models.CASCADE, related_name= "forum_umum")
    time_created = models.DateField(default=timezone.now)

class ForumKhusus(models.Model):
    # user = models.ForeignKey(User,on_delete= models.CASCADE, related_name= "forum_khusus")
    text = models.TextField()
    forum = models.ForeignKey(Forum,on_delete= models.CASCADE, related_name= "forum_khusus")
    time_created = models.DateField(default=timezone.now)