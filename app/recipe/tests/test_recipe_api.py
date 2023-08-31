"""
Tests for recipe APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

from core.constants.mock_data import mock_user, mock_recipe, john_doe


RECIPES_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    """Return recipe detail URL."""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(**recipe):
    """Helper function to save the recipe to the database."""
    return Recipe.objects.create(**recipe)


def create_user(**user):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(**user)


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe APIs."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated recipe APIs."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**john_doe)
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(**mock_recipe(user=self.user, idx=0))
        create_recipe(**mock_recipe(user=self.user, idx=1))

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user."""
        user2 = get_user_model().objects.create_user(**mock_user("Jane", "Doe"))
        create_recipe(**mock_recipe(user=self.user, idx=0))
        create_recipe(**mock_recipe(user=user2, idx=1))

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail."""
        recipe = create_recipe(**mock_recipe(user=self.user, idx=0))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating a recipe."""
        payload = mock_recipe(idx=0)
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        for key in payload:
            self.assertEqual(payload[key], getattr(recipe, key))
        self.assertEqual(recipe.user, self.user)

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch."""
        original_recipe = mock_recipe(user=self.user, idx=0)
        recipe = create_recipe(**mock_recipe(user=self.user, idx=0))
        payload = {"title": "Updated title"}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.description, original_recipe["description"])
        self.assertEqual(recipe.time_minutes, original_recipe["time_minutes"])
        self.assertEqual(recipe.price, original_recipe["price"])
        self.assertEqual(recipe.user, self.user)

    def test_full_update_recipe(self):
        """Test updating a recipe with put."""
        original_recipe = mock_recipe(user=self.user, idx=0)
        recipe = create_recipe(**original_recipe)
        payload = {
            "title": "Updated title",
            "description": "Updated description",
            "time_minutes": 25,
            "price": Decimal("5.99"),
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.description, payload["description"])
        self.assertEqual(recipe.time_minutes, payload["time_minutes"])
        self.assertEqual(recipe.price, payload["price"])
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test that updating the user returns an error."""
        recipe = create_recipe(**mock_recipe(user=self.user, idx=0))
        user2 = get_user_model().objects.create_user(**mock_user("Jane", "Doe"))
        payload = {"user": user2}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe."""
        recipe = create_recipe(**mock_recipe(user=self.user, idx=0))
        url = detail_url(recipe.id)
        self.client.delete(url)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_delete_other_user_recipe_returns_error(self):
        """Test that deleting another user's recipe returns an error."""
        recipe = create_recipe(**mock_recipe(user=self.user, idx=0))
        user2 = get_user_model().objects.create_user(**mock_user("Jane", "Doe"))
        url = detail_url(recipe.id)
        self.client.force_authenticate(user2)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(Recipe.objects.count(), 1)
