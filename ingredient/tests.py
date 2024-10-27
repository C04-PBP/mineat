from django.test import TestCase, Client
from django.urls import reverse
import json
from ingredient.models import Ingredient

class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Tomato")

    def test_ingredient_string_representation(self):
        self.assertEqual(str(self.ingredient), "Tomato")


class IngredientViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("ingredient:record_ingredients")
        self.ingredient = Ingredient.objects.create(name="Ingredient Test")

    def test_show_filter_view(self):
        response = self.client.get(reverse("ingredient:show_filter"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("ingredients", response.context)

    def test_search_ingredient_valid_query(self):
        Ingredient.objects.create(name="Test Ingredient")
        response = self.client.post(reverse("ingredient:search_ingredient"),
                                    data=json.dumps({'ingredient': 'Test'}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        ingredients = json.loads(response.json()['ingredients'])
        self.assertTrue(any("Test Ingredient" in item["fields"]["name"] for item in ingredients))

    def test_record_ingredients_empty(self):
        response = self.client.post(self.url, data=json.dumps({'ingredients': []}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('html', response.json())

    def test_record_ingredients_invalid_data(self):
        response = self.client.post(self.url, data="Invalid JSON", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())
        self.assertEqual(response.json()["status"], "error")