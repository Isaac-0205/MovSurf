from django import forms
from .models import Movie, Genre, Review, Seat, Profile

class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Movie
        fields = ['title', 'description', 'director', 'release_date', 'duration', 'poster', 'trailer_url', 'genres']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.NumberInput(attrs={'min': 1}),
            'trailer_url': forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/embed/...'}),
        }
        help_texts = {
            'duration': 'Duration in minutes',
            'trailer_url': 'YouTube embed URL (e.g., https://www.youtube.com/embed/...)',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
            'comment': forms.Textarea(attrs={'rows': 4})
        }

class AdvancedSearchForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Movie title'}))
    director = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Director name'}))
    min_rating = forms.IntegerField(required=False, min_value=1, max_value=5, widget=forms.NumberInput(attrs={'placeholder': 'Min rating'}))
    min_year = forms.IntegerField(required=False, min_value=1900, max_value=2025, widget=forms.NumberInput(attrs={'placeholder': 'Min year'}))
    max_year = forms.IntegerField(required=False, min_value=1900, max_value=2025, widget=forms.NumberInput(attrs={'placeholder': 'Max year'}))
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    duration_min = forms.IntegerField(required=False, min_value=1, widget=forms.NumberInput(attrs={'placeholder': 'Min duration (min)'}))
    duration_max = forms.IntegerField(required=False, min_value=1, widget=forms.NumberInput(attrs={'placeholder': 'Max duration (min)'}))

class BookingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        showtime = kwargs.pop('showtime', None)
        seat_info = kwargs.pop('seat_info', None)
        super().__init__(*args, **kwargs)
        if showtime and seat_info:
            # Add showtime field
            self.fields['showtime'] = forms.IntegerField(widget=forms.HiddenInput(), initial=showtime.id)
            for seat_id, info in seat_info.items():
                self.fields[f'seat_{seat_id}'] = forms.BooleanField(
                    required=False,
                    label=f'Seat {info["label"]} - ₹{info["price"]}'
                )
    
    def get_selected_seats(self):
        """Return the IDs of selected seats"""
        selected_seats = []
        for field_name, value in self.data.items():
            if field_name.startswith('seat_') and value == 'on':
                try:
                    seat_id = int(field_name.split('_')[1])
                    selected_seats.append(seat_id)
                except (ValueError, IndexError):
                    continue
        return selected_seats

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'date_of_birth']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
