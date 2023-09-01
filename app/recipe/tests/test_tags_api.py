"""
Tests for the tags API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from rest_framework.test import APIClient

from core.models import Tag
from core.constants.mock_data import mock_tag, mock_user, john_doe
from recipe.serializers import TagSerializer


TAGS_URL = reverse("recipe:tag-list")


def detail_url(tag_id):
    """Return tag detail URL."""
    return reverse("recipe:tag-detail", args=[tag_id])


def create_user(**params):
    """Helper function to create a new user."""
    return get_user_model().objects.create_user(**params)


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API."""

    def setUp(self):
        self.user = create_user(**john_doe)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags."""
        Tag.objects.create(user=self.user, **mock_tag())
        Tag.objects.create(user=self.user, **mock_tag())

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user."""
        user2 = create_user(**mock_user())
        Tag.objects.create(user=user2, **mock_tag())
        tag = Tag.objects.create(user=self.user, **mock_tag())

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tag.objects.create(user=self.user, **mock_tag())
        payload = {"name": "New Tag Name"}
        url = detail_url(tag.id)
        self.client.patch(url, payload)

        tag.refresh_from_db()

        self.assertEqual(tag.name, payload["name"])

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(user=self.user, **mock_tag())
        url = detail_url(tag.id)
        self.client.delete(url)

        self.assertEqual(Tag.objects.count(), 0)
