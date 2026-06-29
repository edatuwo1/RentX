from django.contrib import admin
from .models import Car, Booking


# =========================
# CAR ADMIN
# =========================
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'location',
        'price_per_day',
        'available',
        'owner',
    )

    search_fields = (
        'title',
        'location',
    )

    list_filter = (
        'available',
        'location',
    )


# =========================
# BOOKING ADMIN
# =========================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'car',
        'booking_reference',
        'pickup_date',
        'return_date',
    )

    search_fields = (
        'first_name',
        'last_name',
        'booking_reference',
    )