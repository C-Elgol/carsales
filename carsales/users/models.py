from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.templatetags.static import static

from carsales.users.managers import UserManager

class MedicineBaseModel(TimeStampedModel, ActivatorModel):
    """
    Name: CommuneBaseModel
    Description: Abstract base model providing a UUID primary key, soft deletion, activation status, and metadata for all models in the municipal council system.
    Author: ayemeleelgol@gmail.com
    """
    id = models.UUIDField(
        default=uuid.uuid4,
        null=False,
        blank=False,
        unique=True,
        primary_key=True,
        editable=False,
        help_text=_("Unique UUID identifier for the record.")
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text=_("Marks the record as deleted without physically removing it (soft delete).")
    )
    metadata = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        help_text=_("Stores additional metadata in JSON format, such as custom attributes or logs.")
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class User(AbstractBaseUser, MedicineBaseModel, PermissionsMixin):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text=_("User's profile photo.")
    )
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    has_accepted_terms = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone_number"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def get_full_name(self) -> str:
        """Return the user's full name."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
