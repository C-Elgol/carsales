from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from carsales.users.models import CarBaseModel
from carsales.global_data.enum import (
    CarStatusChoices,
    TransmissionChoices,
    FuelTypeChoices,
    BookingStatusChoices,
    PaymentMethodChoices,
    PaymentStatusChoices,
)


class CarBrand(CarBaseModel):
    """
    Represents a car brand (e.g. Toyota, BMW, Honda).
    """
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="brands/logos/", null=True, blank=True)

    class Meta:
        verbose_name = _("Car Brand")
        verbose_name_plural = _("Car Brands")
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarCategory(CarBaseModel):
    """
    Represents car categories such as SUV, Sedan, Hatchback, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Car Category")
        verbose_name_plural = _("Car Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Car(CarBaseModel):
    """
    Represents a car available for rent or sale.
    """
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="cars")
    category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="cars")
    name = models.CharField(max_length=150)
    model_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1980), MaxValueValidator(timezone.now().year + 1)]
    )
    license_plate = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=50)
    seats = models.PositiveIntegerField(default=4)
    transmission = models.CharField(max_length=20, choices=TransmissionChoices.choices, default=TransmissionChoices.AUTOMATIC)
    fuel_type = models.CharField(max_length=20, choices=FuelTypeChoices.choices, default=FuelTypeChoices.PETROL)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Daily rental price"))
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="owned_cars"
    )
    status = models.CharField(max_length=20, choices=CarStatusChoices.choices, default=CarStatusChoices.AVAILABLE)

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.license_plate})"

    @property
    def is_available(self):
        return self.status == CarStatusChoices.AVAILABLE


class CarImage(CarBaseModel):
    """
    Supports multiple images per car.
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cars/images/")
    is_featured = models.BooleanField(default=False, help_text=_("Set as main display image"))

    class Meta:
        verbose_name = _("Car Image")
        verbose_name_plural = _("Car Images")
        ordering = ["-created"]

    def __str__(self):
        return f"Image for {self.car.name}"


class RentalBooking(CarBaseModel):
    """
    Represents a booking made by a user to rent a car.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BookingStatusChoices.choices, default=BookingStatusChoices.PENDING)
    pickup_location = models.CharField(max_length=255, null=True, blank=True)
    dropoff_location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Rental Booking")
        verbose_name_plural = _("Rental Bookings")
        ordering = ["-created"]

    def __str__(self):
        return f"Booking {self.id} - {self.car} ({self.status})"

    def duration_days(self):
        """Calculate the duration of rental in days."""
        return (self.end_date - self.start_date).days

    def save(self, *args, **kwargs):
        """Auto-calculate total price if not provided."""
        if not self.total_price:
            days = self.duration_days()
            self.total_price = days * self.car.daily_rate
        super().save(*args, **kwargs)


class Payment(CarBaseModel):
    """
    Handles payments made for car rentals or purchases.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    booking = models.ForeignKey(RentalBooking, on_delete=models.CASCADE, related_name="payments", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PaymentMethodChoices.choices)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.amount} ({self.status})"


class CarReview(CarBaseModel):
    """
    Customer reviews for rented or purchased cars.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="car_reviews")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Car Review")
        verbose_name_plural = _("Car Reviews")
        unique_together = ("user", "car")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.car.name} ({self.rating}/5)"
