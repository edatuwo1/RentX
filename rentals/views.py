from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Car, Booking
from datetime import datetime
from django.utils import timezone


# =========================
# HOME PAGE
# =========================
def home(request):

    featured_cars = Car.objects.filter(
        available=True
    )[:3]

    return render(
        request,
        'home.html',
        {
            'featured_cars': featured_cars
        }
    )


# =========================
# REGISTER
# =========================
def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully."
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "login.html"
    )


# =========================
# LOGOUT
# =========================
def logout_view(request):

    logout(request)

    return redirect("home")    


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):

    cars = Car.objects.filter(
        owner=request.user
    )

    bookings = Booking.objects.filter(
        car__owner=request.user
    )

    total_vehicles = cars.count()

    available_vehicles = cars.filter(
        available=True
    ).count()

    total_bookings = bookings.count()

    return render(
        request,
        'dashboard.html',
        {
            'total_vehicles': total_vehicles,
            'available_vehicles': available_vehicles,
            'total_bookings': total_bookings,
            'cars': cars.order_by('-created_at')[:3],
            'bookings': bookings.order_by('-created_at')[:3],
        }
    )

# =========================
# MY BOOKINGS
# =========================
@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_bookings.html',
        {
            'bookings': bookings
        }
    )

# =========================
# MY LISTINGS
# =========================
@login_required
def my_listings(request):

    cars = Car.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "my_listings.html",
        {
            "cars": cars
        }
    )



# =========================
# DELETE LISTING
# =========================
@login_required
def delete_listing(request, car_id):

    car = Car.objects.get(
        id=car_id,
        owner=request.user
    )

    car.delete()

    messages.success(
        request,
        "Vehicle deleted successfully."
    )

    return redirect("my_listings")


# =========================
# EDIT LISTING
# =========================
@login_required
def edit_listing(request, car_id):

    car = Car.objects.get(
        id=car_id,
        owner=request.user
    )

    if request.method == "POST":

        car.title = request.POST.get("title")
        car.location = request.POST.get("location")
        car.price_per_day = request.POST.get("price_per_day")

        available = request.POST.get("available")

        car.available = (
            True if available == "on"
            else False
        )

        if request.FILES.get("image"):
            car.image = request.FILES.get("image")

        car.save()

        messages.success(
            request,
            "Vehicle updated successfully."
        )

        return redirect("my_listings")

    return render(
        request,
        "edit_car.html",
        {
            "car": car
        }
    )    


# =========================
# BECOME HOST
# =========================
@login_required
def become_host(request):

    if request.method == "POST":

        title = request.POST.get("title")
        location = request.POST.get("location")
        price_per_day = request.POST.get("price_per_day")

        image = request.FILES.get("image")

        Car.objects.create(
            owner=request.user,
            title=title,
            location=location,
            price_per_day=price_per_day,
            image=image,
            available=True
        )

        messages.success(
            request,
            "Vehicle listed successfully."
        )

        return redirect("my_listings")

    return render(
        request,
        "become_host.html"
    )



# =========================
# BROWSE CARS
# =========================
def browse_cars(request):
    query = request.GET.get("q","")
    cars = Car.objects.all()

    if query:
        cars = cars.filter(
            Q(title__icontains=query) |
        Q(location__icontains=query)
    )

    return render(
        request,
        "browse_cars.html",
        {
            "cars": cars,
            "query": query,
        }
    )


# =========================
# BOOK CAR
# =========================
def book_car(request, car_id):

    car = Car.objects.get(
        id=car_id
    )

    if request.method == "POST":

        # Get dates from form
        pickup_date = datetime.strptime(
            request.POST.get("pickup_date"),
            "%Y-%m-%d"
        ).date()

        return_date = datetime.strptime(
            request.POST.get("return_date"),
            "%Y-%m-%d"
        ).date()

        today = timezone.now().date()

        # Pickup date cannot be in the past
        if pickup_date < today:

            messages.error(
                request,
                "Pickup date cannot be in the past."
            )

            return render(
                request,
                "book_car.html",
                {
                    "car": car
                }
            )

        # Return date must be after pickup date
        if return_date <= pickup_date:

            messages.error(
                request,
                "Return date must be after the pickup date."
            )

            return render(
                request,
                "book_car.html",
                {
                    "car": car
                }
            )

        # Check if vehicle is already booked
        existing_booking = Booking.objects.filter(

            car=car,

            pickup_date__lt=return_date,

            return_date__gt=pickup_date

        ).exists()

        if existing_booking:

            messages.error(

                request,

                "This vehicle is already booked for the selected dates."

            )

            return render(

                request,

                "book_car.html",

                {
                    "car": car
                }

            )

        # Create booking
        booking = Booking.objects.create(

            car=car,

            user=request.user if request.user.is_authenticated else None,

            first_name=request.POST.get("first_name"),

            last_name=request.POST.get("last_name"),

            email=request.POST.get("email"),

            pickup_date=pickup_date,

            return_date=return_date

        )

        return redirect(
            "booking_success",
            booking_id=booking.id
        )

    return render(
        request,
        "book_car.html",
        {
            "car": car
        }
    )
# =========================
# BOOKING SUCCESS
# =========================
def booking_success(request, booking_id):

    booking = Booking.objects.get(
        id=booking_id
    )

    return render(
        request,
        "booking_success.html",
        {
            "booking": booking
        }
    )

# =========================
# BOOKING DETAILS
# =========================
@login_required
def booking_details(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    # Customer OR Host can view
    if (
        booking.user != request.user
        and booking.car.owner != request.user
    ):

        messages.error(
            request,
            "You do not have permission to view this booking."
        )

        return redirect("dashboard")

    return render(
        request,
        "booking_details.html",
        {
            "booking": booking
        }
    )
    
    

# =========================
# MANAGE BOOKING
# =========================

def manage_booking(request):

    booking = None

    if request.method == "POST":

        # NOTE: Get the booking reference entered by the customer.
        reference = request.POST.get(
            "booking_reference"
        )

        # NOTE: Get the customer's last name.
        last_name = request.POST.get(
            "last_name"
        )

        try:

            # NOTE: Both the booking reference and last name
            # must match the same booking.
            #
            # __iexact makes the comparison case-insensitive.
            booking = Booking.objects.get(
                booking_reference__iexact=reference,
                last_name__iexact=last_name
            )

            # NOTE: Save the booking ID in the session so
            # the customer can access the booking details.
            request.session[
                "retrieved_booking"
            ] = booking.id

        except Booking.DoesNotExist:

            # NOTE: If either the reference or last name
            # is incorrect, no booking is returned.
            messages.error(
                request,
                "Booking not found. Please check your booking reference and last name."
            )

    return render(
        request,
        "manage_booking.html",
        {
            "booking": booking
        }
    )


# =========================
# HELP PAGE
# =========================
def help_page(request):

    return render(
        request,
        "help.html"
    )


# =========================
# CONTACT PAGE
# =========================
def contact(request):

    if request.method == "POST":

        messages.success(
            request,
            "Your message has been received."
        )

        return redirect("contact")

    return render(
        request,
        "contact.html"
    )