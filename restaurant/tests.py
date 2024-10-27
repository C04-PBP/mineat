from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from restaurant.models import Restaurant
from location.models import Location
from fnb.models import Fnb
from restaurant.forms import RestaurantForm
import uuid

# Create your tests here.

class RestaurantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create Location and Fnb instances
        self.location = Location.objects.create(name="Test Location", trivia="Trivia about location", image="location_image.jpg")
        self.fnb = Fnb.objects.create(user=self.user, name="Test Fnb", image="fnb_image.jpg", price=100, description="Test Description")
        
        # Create Restaurant instance
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test St",
            location=self.location,
            image="test_image.jpg"
        )
        self.restaurant.fnb.add(self.fnb)

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, "Test Restaurant")
        self.assertEqual(self.restaurant.address, "123 Test St")
        self.assertEqual(self.restaurant.location, self.location)
        self.assertIn(self.fnb, self.restaurant.fnb.all())

class RestaurantViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.location = Location.objects.create(name="Test Location", trivia="Trivia about location", image="location_image.jpg")
        self.fnb = Fnb.objects.create(user=self.user, name="Test Fnb", image="fnb_image.jpg", price=100, description="Test Description")
        
        # Create Restaurant instance
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test St",
            location=self.location,
            image="test_image.jpg"
        )
        self.restaurant.fnb.add(self.fnb)

    def test_show_restaurant_view(self):
        response = self.client.get(reverse("restaurant:show_restaurant"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Restaurant")

    def test_ajax_search_restaurant(self):
        response = self.client.get(reverse("restaurant:ajax_search_restaurant"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Restaurant", response.json()["html"])

    def test_add_restaurant_view(self):
        response = self.client.get(reverse("restaurant:add_restaurant"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_restaurant.html")

    def test_delete_restaurant(self):
        response = self.client.post(reverse("restaurant:delete_restaurant", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Restaurant.objects.filter(id=self.restaurant.id).exists())

    def test_edit_restaurant(self):
        response = self.client.get(reverse("restaurant:edit_restaurant", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_restaurant.html")
        response = self.client.post(reverse("restaurant:edit_restaurant", args=[self.restaurant.id]), {
            "name": "Updated Restaurant",
            "address": "123 Updated St",
            "location": self.location.id,
            "fnb": [self.fnb.id],
            "image": "updated_image.jpg",
        })
        self.assertEqual(response.status_code, 302)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, "Updated Restaurant")

class RestaurantFormTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Test Location", trivia="Trivia about location", image="location_image.jpg")
        self.fnb = Fnb.objects.create(user=User.objects.create_user(username='testuser', password='12345'), name="Test Fnb", image="fnb_image.jpg", price=100, description="Test Description")

    def test_restaurant_form_valid(self):
        form_data = {
            "name": "Form Restaurant",
            "address": "Form Address",
            "location": self.location.id,
            "fnb": [self.fnb.id],
            "image": "form_image.jpg",
        }
        form = RestaurantForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_restaurant_form_invalid(self):
        form_data = {
            "name": "", # Name tidak ada = Invalid
            "address": "Form Address",
            "location": self.location.id,
            "fnb": [self.fnb.id],
            "image": "form_image.jpg",
        }
        form = RestaurantForm(data=form_data)
        self.assertFalse(form.is_valid())