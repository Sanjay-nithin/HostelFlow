from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/profile', ProfileView.as_view()),
     path('services', ServiceListView.as_view()),
    path('bookings', BookingCreateView.as_view()),
    path('bookings/my', MyBookingsView.as_view()),
    path('bookings/availability', get_unavailable_slots),
    path('bookings/<int:booking_id>/cancel', CancelBookingView.as_view()),
    path('bookings/<int:booking_id>/reschedule', RescheduleBookingView.as_view()),
    path('bookings/<int:booking_id>/rate', RateBookingView.as_view()),
    path('bookings/<int:booking_id>/delete', delete_booking, name='delete-booking'),
    path('stats/dashboard', dashboard_stats),
     path('admin/bookings', get_all_bookings),
    path('admin/users', get_all_users),
    path('admin/service-providers', get_service_providers),
    path('admin/service-providers/create', create_service_provider),
    path('admin/service-providers/<str:provider_id>', update_service_provider),
    path('admin/service-providers/<str:provider_id>/delete/', delete_service_provider),
]