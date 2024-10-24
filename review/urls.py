from django.urls import path
from review.views import show_review, add_review, like_review

app_name = 'review'

urlpatterns = [
    path('', show_review, name='show_review'),
    path('add-review/', add_review, name='add_review'),
    path('like-review/', like_review, name='like_review'),
    
]