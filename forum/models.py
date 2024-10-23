from django.db import models
from fnb.models import Fnb
from django.contrib.auth.models import User

# Create your models here.
class Forum(models.Model):
    name = models.CharField(max_length= 255)
    text = models.TextField()
    user = models.ForeignKey(User,on_delete= models.CASCADE, related_name= "forum_umum")

class ForumKhusus(models.Model):
    text = models.TextField()
    forum = models.ForeignKey(Forum,on_delete= models.CASCADE, related_name= "forum_khusus")