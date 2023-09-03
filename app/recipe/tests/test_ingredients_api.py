"""
Tests for the ingredients API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe

from recipe.serializers import IngredientSerializer

from core.constants.mock_data import mock_user, john_doe, mock_ingredient, mock_recipe

INGREDIENTS_URL = reverse("recipe:ingredient-list")


def get_detail_url(ingredient_id):
    """Return the URL for the ingredient detail."""
    return reverse("recipe:ingredient-detail", args=[ingredient_id])


def create_user(**params):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(**params)


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API."""

    def setUp(self):
        """Set up the test client."""
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving ingredients."""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the private ingredients API."""

    def setUp(self):
        """Set up the test client."""
        self.user = create_user(**john_doe)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(user=self.user, name=mock_ingredient(idx=0))
        Ingredient.objects.create(user=self.user, name=mock_ingredient(idx=1))

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returned."""
        user2 = create_user(**mock_user(idx=1))
        Ingredient.objects.create(user=user2, **mock_ingredient(idx=0))
        ingredient = Ingredient.objects.create(user=self.user, **mock_ingredient(idx=1))

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)
        self.assertEqual(res.data[0]["id"], ingredient.id)

    def test_update_ingredient_successful(self):
        """Test updating an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, **mock_ingredient(idx=0))
        payload = {"name": "New Ingredient Name"}
        url = get_detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        ingredient.refresh_from_db()
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(ingredient.name, payload["name"])

    def test_delete_ingredient_successful(self):
        """Test deleting an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, **mock_ingredient(idx=0))
        url = get_detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_filter_ingredients_assigned_to_recipes(self):
        """Test filtering ingredients by those assigned to recipes."""
        i1 = Ingredient.objects.create(user=self.user, **mock_ingredient(idx=0))
        i2 = Ingredient.objects.create(user=self.user, **mock_ingredient(idx=1))
        r1 = Recipe.objects.create(user=self.user, **mock_recipe(name="Recipe 1"))
        r1.ingredients.add(i1)

        res = self.client.get(INGREDIENTS_URL, {"assigned_only": 1})

        s1 = IngredientSerializer(i1)
        s2 = IngredientSerializer(i2)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filter_ingredients_assigned_unique(self):
        """Test filtering ingredients by assigned returns unique items."""
        i1 = Ingredient.objects.create(user=self.user, **mock_ingredient(idx=0))
        Ingredient.objects.create(user=self.user, **mock_ingredient(idx=1))
        r1 = Recipe.objects.create(user=self.user, **mock_recipe(name="Recipe 1"))
        r1.ingredients.add(i1)
        r2 = Recipe.objects.create(user=self.user, **mock_recipe(name="Recipe 2"))
        r2.ingredients.add(i1)

        res = self.client.get(INGREDIENTS_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)
