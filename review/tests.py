
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from fnb.models import Fnb
from review.models import Review

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from fnb.models import Fnb
from review.models import Review

class ReviewTests(TestCase):
    def setUp(self):
        # Setup user and client for authenticated requests
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Setup item makanan sebagai referensi untuk Review, dengan menambahkan 'user'
        self.food_item = Fnb.objects.create(
            name="Sample Food", 
            price=10000, 
            description="Test food item", 
            user=self.user  # Mengisi field user yang dibutuhkan
        )
        
        # Create a sample review object
        self.review = Review.objects.create(
            makanan=self.food_item,
            user=self.user,
            rating=4,
            text="This is a test review"
        )
    
    def test_add_review(self):
        # URL for adding review
        url = reverse('review:add_review')
        
        # Data for review submission
        data = {
            'food_id': self.food_item.id,
            'rating': 5,
            'text': 'Great taste!',
        }
        
        self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(Review.objects.filter(text="Great taste!").exists())

    def test_edit_review(self):
        # URL for editing review
        url = reverse('review:edit_review', args=[self.review.id])
        
        # Data for updating the review
        data = {
            'rating': 3,
            'text': 'Updated review text',
        }
        
        self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Fetch updated review and verify changes
        self.review.refresh_from_db()
        self.assertEqual(self.review.text, 'Updated review text')
        self.assertEqual(self.review.rating, 3)

    def test_delete_review(self):
        # URL for deleting review
        url = reverse('review:delete_review', args=[self.review.id])
        self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
