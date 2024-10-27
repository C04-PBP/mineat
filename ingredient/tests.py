from django.test import TestCase, Client
from django.urls import reverse
import json

class IngredientFilterTests(TestCase):
    def setUp(self):
        # Initialize the Django test client and other setup tasks here
        self.client = Client()
        self.url = reverse('ingredient:record_ingredients')  # Replace with actual URL name if different
    
    def test_search_ingredient_selection(self):
        """Test selecting ingredients and ensuring they are marked as selected."""
        # Simulate the ingredient selection
        selected_ingredients = ["Tomato", "Onion", "Garlic"]
        
        # Send post request with selected ingredients
        response = self.client.post(self.url, data=json.dumps({'ingredients': selected_ingredients}),
                                    content_type="application/json")
        
        # Verify the response status and check if valid HTML is returned in 'html' key of the JSON response
        self.assertEqual(response.status_code, 200)
        self.assertIn('html', response.json())
        self.assertIn("<div", response.json()['html'])  # Simple check for returned HTML structure

    def test_send_selected_ingredient(self):
        """Test sending selected ingredients and verify the returned content is valid food data."""
        # Simulate the selected ingredients
        selected_ingredients = ["Carrot", "Potato", "Pepper"]

        # Post request to send selected ingredients
        response = self.client.post(self.url, data=json.dumps({'ingredients': selected_ingredients}),
                                    content_type="application/json")
        
        # Verify the response status
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        
        # Validate that 'html' field in the response contains relevant food items
        self.assertIn('html', response_data)
        self.assertIn("Fnb", response_data['html'])  # Replace "Food" with a sample expected keyword in food results

    def test_filter_functionality_for_valid_food(self):
        """Test if the filter functionality returns expected valid food based on selected ingredients."""
        selected_ingredients = ["Cassava"]

        response = self.client.post(self.url, data=json.dumps({'ingredients': selected_ingredients}),
                                    content_type="application/json")
        
        # Check if a valid food is returned in response
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('html', response_data)
        # Simple check that ensures a food-related term is within the returned HTML (adjust as needed)
        self.assertIn("div", response_data['html'])  # Replace with the actual expected food item
