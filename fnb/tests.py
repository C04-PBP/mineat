from django.test import TestCase, Client
from django.urls import reverse
from .models import Fnb
from django.contrib.auth.models import User

class FnbModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.fnb = Fnb.objects.create(
            name="Burger",
            description="Tasty burger",
            price=10000,
            user=self.user
        )

    def test_fnb_creation(self):
        """Test the creation of an Fnb instance"""
        self.assertTrue(isinstance(self.fnb, Fnb))
        self.assertEqual(self.fnb.__str__(), self.fnb.name)

    def test_fnb_price(self):
        """Test if price is assigned correctly"""
        self.assertEqual(self.fnb.price, 10000)

class FnbFormTests(TestCase):
    def test_valid_form(self):
        """Test form validation for Fnb creation"""
        data = {
            'name': 'Salad',
            'description': 'Fresh and healthy',
            'price': 7000
        }
        form = FnbForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test form invalidity without all required fields"""
        data = {
            'name': '',
            'description': 'Incomplete item',
            'price': ''
        }
        form = FnbForm(data=data)
        self.assertFalse(form.is_valid())

class FnbViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.fnb = Fnb.objects.create(
            name="Pizza",
            description="Cheesy pizza",
            price=20000,
            user=self.user
        )

    def test_fnb_list_view(self):
        """Test that the list view returns a 200 status and correct template"""
        response = self.client.get(reverse('fnb:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fnb/list.html')

    def test_fnb_detail_view(self):
        """Test the detail view of a single Fnb item"""
        response = self.client.get(reverse('fnb:detail', kwargs={'pk': self.fnb.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.fnb.name)

    def test_fnb_create_view_authenticated(self):
        """Test create view with an authenticated user"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse('fnb:create'), {
            'name': 'New Fnb',
            'description': 'New Description',
            'price': 5000,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Fnb.objects.filter(name="New Fnb").exists())

    def test_fnb_create_view_unauthenticated(self):
        """Test create view without authentication (should redirect)"""
        response = self.client.post(reverse('fnb:create'), {
            'name': 'Unauthorized Fnb',
            'description': 'This should fail',
            'price': 5000,
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Fnb.objects.filter(name="Unauthorized Fnb").exists())

    def test_fnb_update_view(self):
        """Test the update view for an existing Fnb item"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse('fnb:update', kwargs={'pk': self.fnb.pk}), {
            'name': 'Updated Pizza',
            'description': 'Extra cheesy',
            'price': 25000,
        })
        self.assertEqual(response.status_code, 302)
        self.fnb.refresh_from_db()
        self.assertEqual(self.fnb.name, 'Updated Pizza')
        self.assertEqual(self.fnb.price, 25000)

    def test_fnb_delete_view(self):
        """Test the delete view for an Fnb item"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse('fnb:delete', kwargs={'pk': self.fnb.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Fnb.objects.filter(pk=self.fnb.pk).exists())
