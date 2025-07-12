from movies.models import Showtime, Screen, Seat

# Get the first showtime and its screen
showtime = Showtime.objects.first()
screen = showtime.screen

# Add seats for rows A through E, with 10 seats per row
for row in 'ABCDE':
    for num in range(1, 11):
        Seat.objects.create(
            screen=screen,
            row=row,
            number=num,
            seat_type='REG',
            price=100.00
        )
