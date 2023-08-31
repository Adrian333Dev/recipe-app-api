"""
Database models for the application.
"""

from django.conf import settings
from django.db.models import (
    Model,
    CharField,
    TextField,
    EmailField,
    BooleanField,
    IntegerField,
    DecimalField,
    ForeignKey,
    CASCADE,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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

    title = CharField(max_length=255)
    description = TextField(blank=True)
    time_minutes = IntegerField()
    price = DecimalField(max_digits=5, decimal_places=2)
    link = CharField(max_length=255, blank=True)
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
    )

    def __str__(self):
        """Return the string representation of the recipe."""
        return self.title
