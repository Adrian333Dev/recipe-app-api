"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from core.constants.mock_data import mock_user


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Set up the test client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", email="admin@exmaple.com", password="pass12345"
        )
        self.client.force_login(self.admin_user)
        user = mock_user("Test", "User", "3113")
        self.user = get_user_model().objects.create_user(**user)

    def test_users_listed(self):
        """Test that users are listed on user page."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works."""
        url = reverse("admin:core_user_change", args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
