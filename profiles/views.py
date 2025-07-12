from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Service, Booking
from .forms import UserProfileForm, ServiceForm, BookingForm
from django.utils import timezone

@login_required
def profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'profiles/profile.html', {
        'form': form,
        'user_profile': user_profile
    })

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profiles/booking_list.html', {
        'bookings': bookings
    })

@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('profiles:booking_list')
    else:
        form = BookingForm()
    
    return render(request, 'profiles/create_booking.html', {
        'form': form
    })

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
    return redirect('profiles:booking_list')

@login_required
def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'profiles/service_list.html', {
        'services': services
    })
