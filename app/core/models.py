# Database models

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """Custom user manager that supports using email instead of username."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user."""
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # using=self._db is for supporting multiple databases
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        # using=self._db is for supporting multiple databases
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # This is the field that is used to authenticate
    # the user when logging in
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        """Return string representation of the user."""
        return self.email


class Recipe(models.Model):
    """Recipe object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        """Return string representation of the recipe."""
        return self.title


class Tag(models.Model):
    """Tag object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        """Return string representation of the tag."""
        return self.name
