from django.core.management.base import BaseCommand
from movies.models import Theater, Screen, Seat, Showtime
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample theaters, screens, and seats'

    def handle(self, *args, **options):
        # Create sample theaters
        theaters = [
            Theater(name='Cinema World', location='Downtown', capacity=1000),
            Theater(name='MovieMax', location='Uptown', capacity=1200),
            Theater(name='Cineplex', location='Midtown', capacity=1500)
        ]
        Theater.objects.bulk_create(theaters)
        
        # Create screens for each theater
        screens = []
        for theater in theaters:
            for i in range(1, 5):
                screens.append(Screen(theater=theater, number=i, total_seats=200))
        Screen.objects.bulk_create(screens)
        
        # Create seats for each screen
        seat_types = [
            ('REG', 10.00),
            ('PREM', 15.00),
            ('VIP', 20.00)
        ]
        
        seats = []
        for screen in Screen.objects.all():
            # Create rows A through F
            for row in 'ABCDEF':
                # Create seats 1 through 20 in each row
                for seat_num in range(1, 21):
                    seat_type = random.choice(seat_types)
                    seats.append(
                        Seat(
                            screen=screen,
                            row=row,
                            number=seat_num,
                            seat_type=seat_type[0],
                            price=seat_type[1]
                        )
                    )
        Seat.objects.bulk_create(seats)
        
        # Create sample showtimes for movies
        movies = Movie.objects.all()
        for movie in movies:
            for screen in Screen.objects.all():
                # Create showtimes for next 7 days
                for day in range(7):
                    show_date = datetime.now() + timedelta(days=day)
                    # Create morning, afternoon, and evening showtimes
                    for hour in [10, 14, 18]:
                        showtime = Showtime(
                            movie=movie,
                            screen=screen,
                            start_time=show_date.replace(hour=hour, minute=0),
                            available_seats=screen.total_seats
                        )
                        showtime.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data'))
