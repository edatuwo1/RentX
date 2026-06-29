from django.db import models
from django.contrib.auth.models import User
import uuid


# =========================
# CAR MODEL
# =========================
class Car(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cars'
    )

    title = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='cars/'
    )

    available = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================
# BOOKING MODEL
# =========================
class Booking(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    pickup_date = models.DateField()

    return_date = models.DateField()

    booking_reference = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.booking_reference:
            self.booking_reference = (
                str(uuid.uuid4())
                .replace('-', '')
                [:8]
                .upper()
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

        