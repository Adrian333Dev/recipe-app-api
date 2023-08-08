# Tests for the models of the core app.

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

example_user = {
    'email': 'test@example.com',
    'password': 'password123',
    'name': 'Test User'
}


def create_sample_user(email="user@example.com", password="password123"):
    """Create a sample user."""
    return get_user_model().objects.create_user(email, password)


class TestModels(TestCase):
    """Tests for the models of the core app."""

    # ! User Model Tests
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'testpass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without an email raises an error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass123')

    def test_create_new_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpass123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # ! Recipe Model Tests
    def test_create_recipe(self):
        """Test creating a new recipe."""
        user = get_user_model().objects.create_user(**example_user)
        recipe = models.Recipe.objects.create(
            user=user,
            title='Test Recipe',
            time_minutes=5,
            price=Decimal('10.00'),
            description='Test Recipe Description'
        )
        self.assertEqual(recipe.title, 'Test Recipe')
        self.assertEqual(recipe.time_minutes, 5)
        self.assertEqual(recipe.price, Decimal('10.00'))
        self.assertEqual(recipe.description, 'Test Recipe Description')
        self.assertEqual(recipe.user, user)

    # ! Tag Model Tests
    def test_create_tag(self):
        """Test creating a new tag."""
        user = create_sample_user()
        tag = models.Tag.objects.create(
            user=user,
            name='Test Tag'
        )
        self.assertEqual(tag.name, 'Test Tag')
        self.assertEqual(tag.user, user)
