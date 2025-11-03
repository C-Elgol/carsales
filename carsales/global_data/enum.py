from django.db import models
from django.utils.translation import gettext_lazy as _


class CarStatusChoices(models.TextChoices):
    AVAILABLE = "available", _("Available")
    RENTED = "rented", _("Rented")
    SOLD = "sold", _("Sold")
    MAINTENANCE = "maintenance", _("Maintenance")


class TransmissionChoices(models.TextChoices):
    AUTOMATIC = "automatic", _("Automatic")
    MANUAL = "manual", _("Manual")


class FuelTypeChoices(models.TextChoices):
    PETROL = "petrol", _("Petrol")
    DIESEL = "diesel", _("Diesel")
    ELECTRIC = "electric", _("Electric")
    HYBRID = "hybrid", _("Hybrid")


class BookingStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    CONFIRMED = "confirmed", _("Confirmed")
    CANCELLED = "cancelled", _("Cancelled")
    COMPLETED = "completed", _("Completed")


class PaymentMethodChoices(models.TextChoices):
    CREDIT_CARD = "credit_card", _("Credit Card")
    MOBILE_MONEY = "mobile_money", _("Mobile Money")
    CASH = "cash", _("Cash")
    PAYPAL = "paypal", _("PayPal")


class PaymentStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    SUCCESS = "success", _("Success")
    FAILED = "failed", _("Failed")
    REFUNDED = "refunded", _("Refunded")
