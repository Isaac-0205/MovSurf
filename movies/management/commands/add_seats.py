from django.core.management.base import BaseCommand
from movies.models import Showtime, Screen, Seat

class Command(BaseCommand):
    help = 'Add seats to screens'

    def handle(self, *args, **options):
        # Get all screens
        screens = Screen.objects.all()
        
        # Add seats for each screen
        for screen in screens:
            # Premium seats (row A)
            for num in range(1, 11):
                Seat.objects.create(
                    screen=screen,
                    row='A',
                    number=num,
                    seat_type='VIP',
                    price=200.00
                )
        
            # Executive seats (rows B and C)
            for row in 'BC':
                for num in range(1, 11):
                    Seat.objects.create(
                        screen=screen,
                        row=row,
                        number=num,
                        seat_type='PREM',
                        price=150.00
                    )
        
            # Normal seats (rows D and E)
            for row in 'DE':
                for num in range(1, 11):
                    Seat.objects.create(
                        screen=screen,
                        row=row,
                        number=num,
                        seat_type='REG',
                        price=120.00
                    )
            
            self.stdout.write(self.style.SUCCESS(f'Added seats to screen {screen}'))
