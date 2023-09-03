"""
Tests for models.
"""

from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.constants.mock_data import john_doe, mock_user
from core.models import Recipe, Tag, Ingredient
from core import models


def create_user(**params):
    """
    Helper function to create a user.
    """
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):
    """
    Tests for models.
    """

    def test_create_user_successful(self):
        """Test creating a new user is successful."""
        user = create_user(**john_doe)

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
        user = create_user(**mock_user())
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

    def test_create_tags(self):
        """Test creating a new tag."""
        user = create_user(**john_doe)
        tag = Tag.objects.create(user=user, name="Vegan")

        self.assertEqual(str(tag), tag.name)
        self.assertEqual(tag.name, "Vegan")

    def test_create_ingredient(self):
        """Test creating a new ingredient."""
        user = create_user(**john_doe)
        ingredient = Ingredient.objects.create(user=user, name="Cucumber")

        self.assertEqual(str(ingredient), ingredient.name)
        self.assertEqual(ingredient.name, "Cucumber")

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "myimage.jpg")

        expected_path = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(file_path, expected_path)
