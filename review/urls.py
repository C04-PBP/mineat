from django.urls import path
from review.views import show_review, add_review, like_review, load_reviews, load_write_review

app_name = 'review'

urlpatterns = [
    path('', show_review, name='show_review'),
    path('add-review/', add_review, name='add_review'),
    path('like-review/', like_review, name='like_review'),
    path('load_reviews/', load_reviews, name='load_reviews'),
    path('load_write_review/', load_write_review, name='load_write_review'),
    
]