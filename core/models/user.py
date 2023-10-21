from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DefaultUserManager,
)
from django.contrib.auth.hashers import make_password
from uuid import uuid4


class UserManager(DefaultUserManager):
    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str | None = None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Email is required")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields,
    ):
        """Create a new superuser profile"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            email, first_name, last_name, password, **extra_fields
        )


class User(AbstractUser):
    """Authentication User with email as the username field"""

    # Sets the username to None so it's ignored
    username = None
    # Primary key as UUID for security reasons
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # Email field is used for authentication so it must be unique and set as
    # the USERNAME_FIELD
    email = models.EmailField("Unique field for authentication", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        # String representation of a User instance
        return f"{self.email} - {self.get_full_name()}"
