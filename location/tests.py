from django.test import TestCase, Client
from django.urls import reverse
from location.models import Location
import uuid
import json

# Create your tests here.

class LocationModelTest(TestCase):
    def setUp(self):
        # Create a Location instance
        self.location = Location.objects.create(
            name="Test Location",
            trivia="Test trivia about this location.",
            image="test_image.jpg"
        )

    def test_location_creation(self):
        self.assertEqual(self.location.name, "Test Location")
        self.assertEqual(self.location.trivia, "Test trivia about this location.")
        self.assertEqual(self.location.image, "test_image.jpg")


class LocationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(
            name="Test Location",
            trivia="Test trivia about this location.",
            image="test_image.jpg"
        )

    def test_show_location_view(self):
        response = self.client.get(reverse("location:show_location"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Location")
        self.assertTemplateUsed(response, "show_location.html")

    def test_location_details_view(self):
        response = self.client.get(reverse("location:location_details"), {"id": str(self.location.id)})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Location")
        self.assertTemplateUsed(response, "location_details.html")

    def test_location_search_ajax(self):
        response = self.client.get(reverse("location:location_search_ajax"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Location", response.json()["html"])

    def test_update_trivia_view(self):
        new_trivia = "Updated trivia information."
        response = self.client.post(
            reverse("location:update_trivia"),
            data=json.dumps({
                "id": str(self.location.id),
                "trivia": new_trivia
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

        # Refresh the location and check if trivia was updated
        self.location.refresh_from_db()
        self.assertEqual(self.location.trivia, new_trivia)

    def test_update_trivia_invalid_id(self):
        response = self.client.post(
            reverse("location:update_trivia"),
            data=json.dumps({
                "id": str(uuid.uuid4()),  # Non-existing UUID
                "trivia": "New trivia"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["error"], "Location not found")