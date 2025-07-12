from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Review, Watchlist, Booking, Ticket
from .forms import MovieForm, ReviewForm, BookingForm

@login_required
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, 'Movie created successfully')
            return redirect('movies:movie_detail', movie_id=movie.pk)
    else:
        form = MovieForm()
    
    return render(request, 'movies/movie_form.html', {
        'form': form,
        'title': 'Create Movie'
    })
