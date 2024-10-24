from django.db import models
from django.contrib.auth.models import User
from fnb.models import Fnb
import uuid
# Create your models here.
class Review(models.Model):
    makanan = models.ForeignKey(Fnb, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    like = models.IntegerField(default=0)
    
    @property
    def like_count(self):
        return self.likes.count()

class ReviewLike(models.Model):
    review = models.ForeignKey(Review, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('review', 'user')
