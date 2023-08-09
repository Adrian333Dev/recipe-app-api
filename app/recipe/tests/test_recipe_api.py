# Tests for the recipe API

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status  # HTTP status codes
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

example_recipe = {
    'title': 'Example Recipe',
    'time_minutes': 10,
    'price': Decimal('5.00'),
    'description': 'Example description',
    'link': 'https://example.com/recipe',
}

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(**params):
    """Helper function to create a recipe"""
    defaults = example_recipe.copy()
    defaults.update(params)

    return Recipe.objects.create(**defaults)


def create_user(**params):
    """Helper function to create a user"""
    return get_user_model().objects.create_user(**params)


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com', password='password123')
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        other_user = create_user(
            email='other_user@example.com', password='password123')
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = example_recipe.copy()
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in example_recipe.keys():
            self.assertEqual(example_recipe[key], getattr(recipe, key))

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch"""
        recipe = create_recipe(user=self.user, title='Original title')
        payload = {'title': 'New title'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])

    def test_full_update_recipe(self):
        """Test updating a recipe with put"""
        original_recipe = create_recipe(user=self.user, **example_recipe)
        payload = {
            'title': 'New title',
            'time_minutes': 20,
            'price': Decimal('10.00'),
            'description': 'New description',
            'link': 'https://example.com/new-recipe',
        }
        url = detail_url(original_recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe = Recipe.objects.get(id=original_recipe.id)
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_update_recipe_invalid(self):
        """Test updating a recipe with invalid data"""
        new_user = create_user(email='user2@example.com', password='password')
        recipe = create_recipe(user=self.user, **example_recipe)
        payload = {'user': new_user.id}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_try_delete_other_users_recipe(self):
        """Test that a user cannot delete another user's recipe"""
        other_user = create_user(
            email='other_user@example.com', password='password123')
        recipe = create_recipe(user=other_user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)