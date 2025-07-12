from django.core.management.base import BaseCommand
from movies.models import Movie, Genre
import random

class Command(BaseCommand):
    help = 'Create sample movies and genres'

    def handle(self, *args, **options):
        # Create sample genres
        genres = [
            'Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi',
            'Romance', 'Thriller', 'Animation', 'Documentary', 'Adventure'
        ]
        
        # Create genres first
        genre_objects = {}
        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genre_objects[genre_name] = genre
        
        # Create sample movies
        sample_movies = [
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.',
                'director': 'Christopher Nolan',
                'release_date': '2010-07-16',
                'duration': 148,
                'genres': ['Action', 'Sci-Fi', 'Thriller']
            },
            {
                'title': 'The Shawshank Redemption',
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'director': 'Frank Darabont',
                'release_date': '1994-09-23',
                'duration': 142,
                'genres': ['Drama', 'Crime']
            },
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'director': 'Christopher Nolan',
                'release_date': '2008-07-18',
                'duration': 152,
                'genres': ['Action', 'Crime', 'Drama']
            },
            {
                'title': 'Pulp Fiction',
                'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                'director': 'Quentin Tarantino',
                'release_date': '1994-10-14',
                'duration': 154,
                'genres': ['Crime', 'Drama']
            },
            {
                'title': 'The Matrix',
                'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'director': 'Lana Wachowski, Lilly Wachowski',
                'release_date': '1999-03-31',
                'duration': 136,
                'genres': ['Action', 'Sci-Fi']
            }
        ]
        
        for movie_data in sample_movies:
            movie = Movie.objects.create(
                title=movie_data['title'],
                description=movie_data['description'],
                director=movie_data['director'],
                release_date=movie_data['release_date'],
                duration=movie_data['duration']
            )
            
            for genre_name in movie_data['genres']:
                genre = genre_objects.get(genre_name)
                if genre:
                    movie.genres.add(genre)
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
