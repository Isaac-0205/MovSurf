from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    director = models.CharField(max_length=100)
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    trailer_url = models.URLField(blank=True, help_text="YouTube embed URL")
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['movie', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.rating} stars"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class Theater(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name

class Screen(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    number = models.IntegerField()
    total_seats = models.IntegerField()
    
    def __str__(self):
        return f"Screen {self.number} - {self.theater.name}"

class Seat(models.Model):
    SCREEN_TYPES = (
        ('REG', 'Normal'),  # Changed from Regular to Normal
        ('PREM', 'Executive'),
        ('VIP', 'Premium'),
    )
    
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)
    number = models.IntegerField()
    seat_type = models.CharField(max_length=4, choices=SCREEN_TYPES, default='REG')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('screen', 'row', 'number')
        
    def __str__(self):
        return f"{self.screen} - Row {self.row} Seat {self.number}"

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    available_seats = models.IntegerField()
    
    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.start_time + timezone.timedelta(minutes=self.movie.duration)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.movie.title} - {self.screen} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_bookings', null=True, blank=True)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed')
        ],
        default='pending'
    )
    
    def __str__(self):
        return f"Booking #{self.id} - {self.showtime}"

class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('booking', 'seat')
        
    def __str__(self):
        return f"Ticket for {self.booking.showtime.movie.title} - Seat {self.seat}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='movie_profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default-profile.png'
