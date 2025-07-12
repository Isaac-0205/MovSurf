from django.core.management.base import BaseCommand
from movies.models import Genre

class Command(BaseCommand):
    help = 'Create default movie genres'

    def handle(self, *args, **options):
        genres = [
            'Action',
            'Adventure',
            'Animation',
            'Comedy',
            'Crime',
            'Drama',
            'Fantasy',
            'Horror',
            'Mystery',
            'Romance',
            'Sci-Fi',
            'Thriller',
            'Western'
        ]

        for genre_name in genres:
            Genre.objects.get_or_create(name=genre_name)

        self.stdout.write(self.style.SUCCESS('Successfully created default genres'))
