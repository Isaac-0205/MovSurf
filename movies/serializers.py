from rest_framework import serializers
from .models import Movie, Genre, Review, Watchlist, Theater, Screen, Seat, Showtime, Booking, Ticket

# Core Models
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'director', 'release_date', 'duration', 'trailer_url', 'poster', 'genres']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    
    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'added_at']

# Booking System Models
class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ['id', 'name', 'location', 'capacity']

class ScreenSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer()
    
    class Meta:
        model = Screen
        fields = ['id', 'theater', 'number', 'total_seats']

class SeatSerializer(serializers.ModelSerializer):
    screen = ScreenSerializer()
    
    class Meta:
        model = Seat
        fields = ['id', 'screen', 'row', 'number', 'seat_type', 'price']

class ShowtimeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    screen = ScreenSerializer()
    
    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'screen', 'start_time', 'end_time', 'available_seats']

class TicketSerializer(serializers.ModelSerializer):
    seat = SeatSerializer()
    
    class Meta:
        model = Ticket
        fields = ['id', 'seat', 'price']

class BookingSerializer(serializers.ModelSerializer):
    showtime = ShowtimeSerializer()
    tickets = TicketSerializer(many=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'showtime', 'booking_time', 'total_amount', 'status', 'tickets']
