# Tests for user API.

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

example_user = {
    'email': 'test@example.com',
    'password': 'password123',
    'name': 'Test User'
}


def create_user(**params):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)."""

    def setUp(self):
        """Set up the test client."""
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating user with valid payload is successful."""
        # copy the example_user dict to avoid changing it
        payload = example_user.copy()
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_with_existing_email(self):
        """Test creating user with existing email fails."""
        payload = example_user.copy()
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password(self):
        """Test creating user with short password fails."""
        payload = example_user.copy()
        payload['password'] = 'pw'
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user."""
        user_data = example_user.copy()
        create_user(**user_data)
        payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given."""
        user_data = example_user.copy()
        create_user(**user_data)
        payload = {
            'email': user_data['email'],
            'password': 'wrongpassword'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
