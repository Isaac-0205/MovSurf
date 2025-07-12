from django import forms
from .models import UserProfile, Service, Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4})
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration_minutes', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'booking_date', 'booking_time']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
