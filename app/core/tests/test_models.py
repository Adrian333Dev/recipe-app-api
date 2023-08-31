"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.constants.mock_data import john_doe, mock_user
from core.models import Recipe


class ModelTests(TestCase):
    """
    Tests for models.
    """

    def test_create_user_successful(self):
        """Test creating a new user is successful."""
        user = get_user_model().objects.create_user(**john_doe)

        self.assertEqual(user.email, john_doe["email"])
        self.assertEqual(user.username, john_doe["username"])
        self.assertTrue(user.check_password(john_doe["password"]))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        SAMPLE_EMAILS = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        SAMPLE_USERNAMES = ["test1", "test2", "test3", "test4"]

        for i, emails in enumerate(SAMPLE_EMAILS):
            email, expected = emails
            user = get_user_model().objects.create_user(
                email=email,
                username=SAMPLE_USERNAMES[i],
                password=john_doe["password"],
            )

            self.assertEqual(user.email, expected)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                username=john_doe["username"],
                password=john_doe["password"],
            )

    def test_new_user_invalid_username(self):
        """Test creating user with no username raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=john_doe["email"],
                username=None,
                password=john_doe["password"],
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            email=john_doe["email"],
            username=john_doe["username"],
            password=john_doe["password"],
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a new recipe."""
        user = get_user_model().objects.create_user(**mock_user("Alice", "Benjamin"))
        recipe = Recipe.objects.create(
            user=user,
            title="Steak and mushroom sauce",
            time_minutes=5,
            price=Decimal("5.00"),
            description="How to make steak and mushroom sauce",
        )

        self.assertEqual(recipe.user, user)
        self.assertEqual(str(recipe), recipe.title)
        self.assertEqual(recipe.title, "Steak and mushroom sauce")
        self.assertEqual(recipe.time_minutes, 5)
        self.assertEqual(recipe.price, Decimal("5.00"))
