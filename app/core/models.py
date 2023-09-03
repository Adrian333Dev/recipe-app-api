"""
Database models for the application.
"""

import uuid
import os

from django.conf import settings
from django.db.models import (
    Model,
    CharField,
    TextField,
    EmailField,
    BooleanField,
    IntegerField,
    DecimalField,
    ImageField,
    ForeignKey,
    ManyToManyField,
    CASCADE,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

AUTH_USER_MODEL = settings.AUTH_USER_MODEL


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "recipe", filename)


class UserManager(BaseUserManager):
    """User manager for the application."""

    def create_user(self, email, username, password=None, **extra_fields):
        """Create a new user for the application."""
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Create a new superuser for the application."""
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        if not password:
            raise ValueError("Users must have a password.")

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model for the application."""

    first_name = CharField(max_length=25)
    last_name = CharField(max_length=25)
    username = CharField(max_length=50, unique=True)
    email = EmailField(max_length=255, unique=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Recipe(Model):
    """Recipe model for the application."""

    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    title = CharField(max_length=255)
    description = TextField(blank=True)
    time_minutes = IntegerField()
    price = DecimalField(max_digits=5, decimal_places=2)
    link = CharField(max_length=255, blank=True)
    tags = ManyToManyField("Tag")
    ingredients = ManyToManyField("Ingredient")
    image = ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        """Return the string representation of the recipe."""
        return self.title


class Tag(Model):
    """Tag model for the application."""

    name = CharField(max_length=255)
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        """Return the string representation of the tag."""
        return self.name


class Ingredient(Model):
    """Ingredient model for the application."""

    name = CharField(max_length=255)
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        """Return the string representation of the ingredient."""
        return self.name
