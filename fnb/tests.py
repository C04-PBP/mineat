from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from fnb.models import Fnb
from ingredient.models import Ingredient
import uuid
import json

# Create your tests here.

class FnbModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.fnb = Fnb.objects.create(
            user=self.user,
            name="Test Fnb",
            image="test_image.jpg",
            price=100,
            description="Test Fnb Description"
        )

    def test_fnb_creation(self):
        self.assertEqual(self.fnb.name, "Test Fnb")
        self.assertEqual(self.fnb.price, 100)
        self.assertEqual(self.fnb.description, "Test Fnb Description")

    def test_fnb_string_representation(self):
        self.assertEqual(str(self.fnb), "Test Fnb")


class FnbViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        self.ingredient2 = Ingredient.objects.create(name="Ingredient 2")
        self.fnb = Fnb.objects.create(
            user=self.user,
            name="Test Fnb",
            image="test_image.jpg",
            price=100,
            description="Test Fnb Description"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_show_fnb_view(self):
        response = self.client.get(reverse("fnb:show_fnb"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Fnb")
        self.assertTemplateUsed(response, "show_fnb.html")

    def test_add_fnb_view(self):
        response = self.client.post(reverse("fnb:add_fnb"), {
            "name": "New Fnb",
            "description": "New Description",
            "price": 200,
            "ingredients": [self.ingredient1.id, self.ingredient2.id]  # Select ingredients
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        new_fnb = Fnb.objects.get(name="New Fnb")
        self.assertTrue(new_fnb)

        # Check if ingredients are linked to the Fnb
        self.assertEqual(new_fnb.fnb.count(), 2)

    def test_edit_fnb_view(self):
        response = self.client.post(reverse("fnb:edit_fnb", args=[self.fnb.id]), {
            "name": "Updated Fnb",
            "description": "Updated Description",
            "price": 150,
            "ingredients": [self.ingredient1.id]
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.fnb.refresh_from_db()
        self.assertEqual(self.fnb.name, "Updated Fnb")
        self.assertEqual(self.fnb.price, 150)

    def test_delete_fnb_view(self):
        response = self.client.post(reverse("fnb:delete_fnb", args=[self.fnb.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Fnb.objects.filter(id=self.fnb.id).exists())

    def test_search_fnbs(self):
        response = self.client.get(reverse("fnb:search_fnbs"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Fnb", response.json()["html"])

    def test_add_fnb_ajax_authenticated(self):
        response = self.client.post(reverse("fnb:add_fnb_ajax"), {
            "name": "AJAX Fnb",
            "description": "Description for AJAX",
            "price": 300,
            "image": "ajax_image.jpg"
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Fnb.objects.filter(name="AJAX Fnb").exists())

    def test_add_fnb_ajax_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse("fnb:add_fnb_ajax"), {
            "name": "AJAX Fnb",
            "description": "Description for AJAX",
            "price": 300,
            "image": "ajax_image.jpg"
        })
        self.assertEqual(response.status_code, 403)

    def test_show_json(self):
        response = self.client.get(reverse("fnb:show_json"))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertTrue(any(item["fields"]["name"] == "Test Fnb" for item in json_data))