from django.contrib import admin
from .models import Movie, Genre, Review, Watchlist, Theater, Screen, Seat, Showtime, Booking, Ticket

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_date', 'duration')
    search_fields = ('title', 'director')
    list_filter = ('release_date', 'genres')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'added_at')
    list_filter = ('user',)

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity')
    search_fields = ('name', 'location')

@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ('theater', 'number', 'total_seats')
    list_filter = ('theater',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('screen', 'row', 'number', 'seat_type', 'price')
    list_filter = ('screen', 'seat_type')

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'screen', 'start_time', 'end_time', 'available_seats')
    list_filter = ('start_time', 'screen__theater')
    search_fields = ('movie__title', 'screen__theater__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'showtime', 'booking_time', 'total_amount', 'status')
    list_filter = ('status', 'booking_time')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('booking', 'seat', 'price')
    list_filter = ('booking__showtime__movie',)
