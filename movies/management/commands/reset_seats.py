from django.core.management.base import BaseCommand
from movies.models import Seat

class Command(BaseCommand):
    help = 'Delete all seats and add new ones'

    def handle(self, *args, **options):
        # Delete all existing seats
        Seat.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all existing seats'))
        
        # Run the add_seats command
        from django.core.management import call_command
        call_command('add_seats')
        
        self.stdout.write(self.style.SUCCESS('Successfully reset and added new seats'))
