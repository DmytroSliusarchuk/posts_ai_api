from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(APITestCase):
    def test_user_registration(self):
        url = reverse("register")
        data = {
            "username": "testuser",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "auto_response_enabled": True,
            "auto_response_delay": 5,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login(self):
        User.objects.create_user(
            username="testuser", password="testpass123", email="test1@email.com"
        )

        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
