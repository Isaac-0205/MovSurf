from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'watchlist', views.WatchlistViewSet)
router.register(r'theaters', views.TheaterViewSet)
router.register(r'screens', views.ScreenViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'showtimes', views.ShowtimeViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'tickets', views.TicketViewSet)

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    # Movie detail view with debug info
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('movie/<int:movie_id>/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('movie/<int:movie_id>/book/', views.book_movie, name='book_movie'),
    path('movie/<int:movie_id>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('movie/<int:movie_id>/remove_from_watchlist/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('add_movie/', views.create_movie, name='create_movie'),
    path('booking/', views.booking, name='booking'),
    path('booking/select_showtime/<int:movie_id>/', views.select_showtime, name='select_showtime'),
    path('booking/book_movie/<int:showtime_id>/', views.book_movie, name='book_movie'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('movie/<int:movie_id>/add_review/', views.review_create, name='add_review'),
    path('movie/<int:movie_id>/review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('movie/<int:movie_id>/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('movie/<int:movie_id>/review/<int:review_id>/', views.view_review, name='view_review'),
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True,
        extra_context={'next': 'movies:movie_list'}
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='movies:movie_list'
    ), name='logout'),
    path('debug/media/', views.debug_media, name='debug_media'),
    path('register/', views.register, name='register'),
    path('movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('movie/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
]
