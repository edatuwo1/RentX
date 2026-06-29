from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Car, Booking


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

    car = Car.objects.get(id=car_id)

    if request.method == "POST":

        booking=Booking.objects.create(
            car=car,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            pickup_date=request.POST.get("pickup_date"),
            return_date=request.POST.get("return_date")
        )

        return redirect("booking_success",
        booking_id=booking.id)

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
# RETRIEVE BOOKING
# =========================
def retrieve_booking(request):

    booking = None

    if request.method == "POST":

        reference = request.POST.get(
            "booking_reference"
        )

        try:

            booking = Booking.objects.get(
                booking_reference=reference
            )

        except Booking.DoesNotExist:

            messages.error(
                request,
                "Booking not found."
            )

    return render(
        request,
        "retrieve_booking.html",
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

        reference = request.POST.get(
            "booking_reference"
        )

        try:

            booking = Booking.objects.get(
                booking_reference=reference
            )

        except Booking.DoesNotExist:

            messages.error(
                request,
                "Booking not found."
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