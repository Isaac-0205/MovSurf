from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth import login
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MovieSerializer, GenreSerializer, ReviewSerializer, WatchlistSerializer
from .serializers import TheaterSerializer
from .serializers import ScreenSerializer
from .serializers import SeatSerializer
from .serializers import ShowtimeSerializer
from .serializers import BookingSerializer
from .serializers import TicketSerializer
from .models import Movie, Genre, Review, Watchlist, Theater, Screen, Seat, Showtime, Booking, Ticket
from .forms import MovieForm, ReviewForm, AdvancedSearchForm, BookingForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
import os
import pprint

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return Response({'detail': 'Only staff users can create movies'}, 
                          status=status.HTTP_403_FORBIDDEN)
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        movies = Movie.objects.filter(
            models.Q(title__icontains=query) | 
            models.Q(director__icontains=query)
        )
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

def watchlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    watchlisted_movies = Watchlist.objects.filter(user=request.user)
    return render(request, 'movies/watchlist.html', {
        'watchlisted_movies': watchlisted_movies
    })

def view_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    watchlisted_movies = Watchlist.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    
    return render(request, 'movies/profile.html', {
        'watchlisted_movies': watchlisted_movies,
        'reviews': reviews
    })

def create_movie(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.created_by = request.user
            movie.save()
            form.save_m2m()
            return redirect('movies:movie_detail', pk=movie.pk)
    else:
        form = MovieForm()
    
    return render(request, 'movies/create_movie.html', {'form': form})

def add_to_watchlist(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    movie = get_object_or_404(Movie, pk=movie_id)
    Watchlist.objects.create(user=request.user, movie=movie)
    return redirect('movies:movie_detail', movie_id=movie_id)

def remove_from_watchlist(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    movie = get_object_or_404(Movie, pk=movie_id)
    Watchlist.objects.filter(user=request.user, movie=movie).delete()
    return redirect('movies:movie_detail', pk=movie_id)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScreenViewSet(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer
    permission_classes = [permissions.IsAuthenticated]

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(booking__user=self.request.user)

def home(request):
    movies = Movie.objects.all().order_by('-created_at')[:12]
    genres = Genre.objects.all()
    return render(request, 'movies/home.html', {
        'movies': movies,
        'genres': genres
    })

def movie_list(request):
    movies = Movie.objects.all()
    
    # Handle advanced search
    form = AdvancedSearchForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        
        if data['title']:
            movies = movies.filter(title__icontains=data['title'])
        if data['director']:
            movies = movies.filter(director__icontains=data['director'])
        if data['min_rating']:
            movies = movies.annotate(avg_rating=models.Avg('reviews__rating'))
            movies = movies.filter(avg_rating__gte=data['min_rating'])
        if data['min_year']:
            movies = movies.filter(release_date__year__gte=data['min_year'])
        if data['max_year']:
            movies = movies.filter(release_date__year__lte=data['max_year'])
        if data['genres']:
            movies = movies.filter(genres__in=data['genres'])
        if data['duration_min']:
            movies = movies.filter(duration__gte=data['duration_min'])
        if data['duration_max']:
            movies = movies.filter(duration__lte=data['duration_max'])
    
    # Handle simple search
    search_query = request.GET.get('q')
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(director__icontains=search_query)
        )
    
    # Filter by genre
    genre_id = request.GET.get('genre')
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
    
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'movies/movie_list.html', {
        'page_obj': page_obj,
        'genres': Genre.objects.all(),
        'form': form
    })

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'Movie "{movie.title}" has been added successfully!')
            return redirect('movies:movie_detail', movie_id=movie.id)
    else:
        form = MovieForm()
    
    return render(request, 'movies/add_movie.html', {
        'form': form
    })

def movie_detail(request, movie_id):
    print("\n=== DEBUG: movie_detail view called ===")
    print(f"Requested movie_id: {movie_id}")
    print(f"User: {request.user}")
    print(f"Is authenticated: {request.user.is_authenticated}")
    
    # Debug: List all movies in the database
    all_movies = Movie.objects.all()
    print("\n=== Movies in database ===")
    for m in all_movies:
        print(f"ID: {m.id}, Title: {m.title}")
    
    try:
        movie = get_object_or_404(Movie, pk=movie_id)
        print(f"Found movie: {movie.title} (ID: {movie.id})")
        
        reviews = movie.reviews.all().order_by('-created_at')
        showtimes = Showtime.objects.filter(movie=movie, start_time__gte=timezone.now()).order_by('start_time')
        
        if request.method == 'POST' and request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.movie = movie
                review.user = request.user
                review.save()
                messages.success(request, 'Review added successfully')
                return redirect('movies:movie_detail', movie_id=movie_id)
        else:
            form = ReviewForm()
        
        return render(request, 'movies/movie_detail.html', {
            'movie': movie,
            'reviews': reviews,
            'showtimes': showtimes,
            'form': form,
            'is_in_watchlist': Watchlist.objects.filter(user=request.user, movie=movie).exists() if request.user.is_authenticated else False
        })
        
    except Exception as e:
        print(f"\n=== ERROR in movie_detail view ===")
        print(str(e))
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('movies:movie_list')

@login_required
def watchlist(request):
    watchlisted_movies = Watchlist.objects.filter(user=request.user)
    print(f"Watchlist items count: {watchlisted_movies.count()}")
    print(f"Watchlist items: {watchlisted_movies}")
    return render(request, 'movies/watchlist.html', {
        'watchlisted_movies': watchlisted_movies
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('movies:movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {
        'form': form
    })

@login_required
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    if created:
        messages.success(request, f'Added {movie.title} to your watchlist!')
    else:
        messages.info(request, f'{movie.title} is already in your watchlist!')
    return redirect('movies:movie_detail', movie_id=movie_id)

@login_required
def search_movies(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(director__icontains=query)
    ).distinct()
    
    return render(request, 'movies/search_results.html', {
        'movies': movies,
        'query': query
    })

@login_required
def book_movie(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, showtime=showtime)
        if form.is_valid():
            # Create booking
            selected_seats = form.get_selected_seats()
            seats = Seat.objects.filter(id__in=selected_seats, screen=showtime.screen)
            total_amount = sum(seat.price for seat in seats)
            
            booking = Booking.objects.create(
                user=request.user,
                showtime=showtime,
                total_amount=total_amount,
                status='pending'
            )
            
            # Create tickets for selected seats
            for seat_id in form.get_selected_seats():
                seat = Seat.objects.get(id=seat_id, screen=showtime.screen)
                Ticket.objects.create(
                    booking=booking,
                    seat=seat,
                    price=seat.price
                )
            
            messages.success(request, 'Booking created successfully')
            return redirect('movies:booking_confirmation', booking_id=booking.pk)
    else:
        # Get all seats for this showtime's screen
        seats = Seat.objects.filter(screen=showtime.screen)
        print(f"Number of seats found: {seats.count()}")
        print("=== DEBUG: All seat types in this screen ===")
        for seat in seats:
            print(f"Seat ID: {seat.id}, Row: {seat.row}, Number: {seat.number}, Type: {seat.seat_type!r}, Price: {seat.price}")
        
        # Map old codes to new display names
        seat_type_map = {
            'REG': 'Normal',
            'PREM': 'Executive',
            'VIP': 'Premium',
            'Normal': 'Normal',
            'Executive': 'Executive',
            'Premium': 'Premium',
        }
        seat_info = {'Normal': {}, 'Executive': {}, 'Premium': {}}
        for seat in seats:
            seat_type = seat_type_map.get(seat.seat_type)
            if seat_type is None:
                continue  # skip unknown types
            if seat.row not in seat_info[seat_type]:
                seat_info[seat_type][seat.row] = []
            seat_info[seat_type][seat.row].append({
                'id': seat.id,
                'number': seat.number,
                'label': f'{seat.row}{seat.number}',
                'price': seat.price,
            })
        print('=== DEBUG: seat_info structure ===')
        pprint.pprint(seat_info)
        # Create form with seat_info (flattened for BookingForm compatibility)
        flat_seat_info = {
            seat.id: {
                'seat_type': seat.seat_type,
                'price': seat.price,
                'label': f'Seat {seat.row}{seat.number} ({seat.seat_type}) - ₹{seat.price}'
            }
            for seat in seats
        }
        form = BookingForm(showtime=showtime, seat_info=flat_seat_info)
        return render(request, 'movies/book_movie.html', {
            'form': form,
            'showtime': showtime,
            'seat_info': seat_info
        })

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    tickets = booking.ticket_set.all()
    
    return render(request, 'movies/booking_confirmation.html', {
        'booking': booking,
        'tickets': tickets
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_time')
    
    return render(request, 'movies/my_bookings.html', {
        'bookings': bookings
    })

@login_required
def view_profile(request):
    user = request.user
    try:
        profile = user.movie_profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    watchlisted_movies = Watchlist.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'movies/profile.html', {
        'user': user,
        'profile': profile,
        'watchlisted_movies': watchlisted_movies,
        'reviews': reviews
    })

@login_required
def booking(request):
    movies = Movie.objects.all()
    return render(request, 'movies/booking.html', {'movies': movies})

@login_required
def select_showtime(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(
        movie=movie,
        start_time__gte=timezone.now()
    ).order_by('start_time')
    
    return render(request, 'movies/select_showtime.html', {
        'movie': movie,
        'showtimes': showtimes
    })

@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.movie_profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('movies:view_profile')
    else:
        user_form = UserChangeForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    
    return render(request, 'movies/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def edit_movie(request, movie_id):
    try:
        movie = get_object_or_404(Movie, pk=movie_id)
        
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                movie = form.save()
                messages.success(request, 'Movie updated successfully')
                return redirect('movies:movie_detail', movie_id=movie.id)
        else:
            form = MovieForm(instance=movie)
        
        return render(request, 'movies/movie_form.html', {
            'form': form,
            'title': f'Edit {movie.title}'
        })
        
    except Exception as e:
        messages.error(request, f'Error editing movie: {str(e)}')
        return redirect('movies:movie_detail', movie_id=movie_id)

@login_required
def watchlist_remove(request, movie_id):
    watchlist_item = get_object_or_404(Watchlist, movie_id=movie_id, user=request.user)
    movie_title = watchlist_item.movie.title
    watchlist_item.delete()
    messages.success(request, f'Removed {movie_title} from your watchlist!')
    return redirect('movies:watchlist')

@login_required
def edit_review(request, movie_id, review_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    review = get_object_or_404(Review, pk=review_id, user=request.user, movie=movie)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully')
            return redirect('movies:movie_detail', pk=movie_id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'movies/edit_review.html', {
        'form': form,
        'movie': movie
    })

@login_required
def view_review(request, movie_id, review_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    review = get_object_or_404(Review, pk=review_id, movie=movie)
    
    return render(request, 'movies/view_review.html', {
        'movie': movie,
        'review': review
    })

@login_required
def delete_review(request, movie_id, review_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    review = get_object_or_404(Review, pk=review_id, user=request.user, movie=movie)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully')
        return redirect('movies:movie_detail', pk=movie_id)
    
    return render(request, 'movies/confirm_delete_review.html', {
        'review': review,
        'movie': movie
    })

@login_required
@permission_required('movies.change_movie', raise_exception=True)
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            messages.success(request, 'Movie updated successfully')
            return redirect('movies:movie_detail', pk=pk)
    else:
        form = MovieForm(instance=movie)
    
    return render(request, 'movies/movie_form.html', {
        'form': form,
        'title': 'Edit Movie'
    })

@login_required
@login_required
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, 'Movie created successfully')
            return redirect('movies:movie_detail', movie_id=movie.id)
    else:
        form = MovieForm()
    
    return render(request, 'movies/movie_form.html', {
        'form': form,
        'title': 'Create Movie'
    })

@login_required
def delete_movie(request, movie_id):
    try:
        movie = get_object_or_404(Movie, pk=movie_id)
        
        if request.method == 'POST':
            movie_title = movie.title
            movie.delete()
            messages.success(request, f'Movie "{movie_title}" was deleted successfully')
            return redirect('movies:movie_list')
        
        return render(request, 'movies/confirm_delete.html', {
            'movie': movie,
            'title': f'Delete {movie.title}'
        })
        
    except Exception as e:
        messages.error(request, f'Error deleting movie: {str(e)}')
        return redirect('movies:movie_detail', movie_id=movie_id)

@login_required
def review_create(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully.')
            return redirect('movie_detail', pk=pk)
    else:
        form = ReviewForm()
    
    return render(request, 'movies/review_form.html', {
        'form': form,
        'movie': movie
    })

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user == request.user:
        movie_id = review.movie_id
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('movies:movie_detail', pk=movie_id)
    else:
        return HttpResponseForbidden()

@login_required
@permission_required('movies.delete_movie', raise_exception=True)
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully')
        return redirect('movies:movie_list')
    return render(request, 'movies/confirm_delete.html', {'movie': movie})

def debug_media(request):
    """Debug view to check media configuration and test image URLs"""
    context = {
        'media_root': settings.MEDIA_ROOT,
        'media_url': settings.MEDIA_URL,
        'static_url': settings.STATIC_URL,
        'debug': settings.DEBUG,
        'all_media_files': [],
        'test_files': []
    }
    
    # List all files in media directory
    try:
        media_dir = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), media_dir)
                context['all_media_files'].append({
                    'path': rel_path,
                    'url': os.path.join(settings.MEDIA_URL, rel_path).replace('\\', '/')
                })
    except Exception as e:
        context['error'] = f"Error reading media directory: {str(e)}"
    
    # Test file access
    test_files = [
        'movie_posters/Screenshot_2025-04-28-02-03-39-99_92460851df6f172a4592fca41cc2d2e6.jpg',
        'movie_posters/Screenshot_2025-05-02_151115.png'
    ]
    
    for test_file in test_files:
        full_path = os.path.join(settings.MEDIA_ROOT, test_file)
        exists = os.path.exists(full_path)
        context['test_files'].append({
            'path': test_file,
            'full_path': full_path,
            'exists': exists,
            'url': os.path.join(settings.MEDIA_URL, test_file).replace('\\', '/')
        })
    
    return render(request, 'movies/debug_media.html', context)
