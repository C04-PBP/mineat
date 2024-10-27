from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Forum, ForumKhusus
from django.utils import timezone
import json

# Create your tests here.
class ForumTests(TestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Create sample data for testing
        self.forum = Forum.objects.create(
            name="Test Forum",
            text="This is a test forum.",
            user=self.user,
            time_created=timezone.now()
        )
        
        self.forum_khusus = ForumKhusus.objects.create(
            text="This is a comment in the forum.",
            user=self.user,
            forum=self.forum,
            time_created=timezone.now()
        )

    def test_show_forum_view(self):
        # Test the show_forum view without filters
        response = self.client.get(reverse('forum:show-forum-umum'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Forum")

    def test_show_forum_view_with_filter(self):
        # Test the show_forum view with unanswered filter
        response = self.client.get(reverse('forum:show-forum-umum') + '?filter_unanswered=true')
        self.assertEqual(response.status_code, 200)

    def test_add_forum_view(self):
        # Test adding a forum with valid data
        data = {
            'name': 'New Forum',
            'comment': 'This is a new comment.'
        }
        response = self.client.post(
            reverse('forum:add-forum'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Forum.objects.filter(name="New Forum").exists())

    def test_add_forum_khusus_view(self):
        # Test adding a forum_khusus comment to an existing forum
        data = {
            'comment': 'This is another test comment.'
        }
        response = self.client.post(
            reverse('forum:forum-khusus', args=[self.forum.id]),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ForumKhusus.objects.filter(text="This is another test comment.").exists())

    def test_add_forum_invalid_data(self):
        # Test adding a forum with invalid data
        data = {
            'name': '',  # Empty name should fail
            'comment': ''
        }
        response = self.client.post(
            reverse('forum:add-forum'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_logout_redirect(self):
        # Test logout and redirection to the landing page
        response = self.client.get(reverse('fnb:logout'))
        self.assertEqual(response.status_code, 302)  # Check redirection
