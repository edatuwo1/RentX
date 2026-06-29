from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('become-host/', views.become_host, name='become_host'),

    path('browse/', views.browse_cars, name='browse_cars'),

    path('delete-listing/<int:car_id>/', views.delete_listing, name='delete_listing'),

    path('edit-listing/<int:car_id>/', views.edit_listing, name='edit_listing'),

    path('book-car/<int:car_id>/', views.book_car, name='book_car'),
    
    path('booking-success/<int:booking_id>/',views.booking_success,name='booking_success'),

    path('retrieve-booking/',views.retrieve_booking,name='retrieve_booking'),

    path('manage-booking/',views.manage_booking,name='manage_booking'),

    path('help/',views.help_page,name='help'),

    path('contact/',views.contact,name='contact'),
]