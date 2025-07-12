from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('services/', views.service_list, name='service_list'),
]
