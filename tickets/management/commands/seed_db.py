from django.core.management.base import BaseCommand
from tickets.models import Event

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        event, created = Event.objects.get_or_create(
            id=1,
            defaults={
                'name': 'Concert',
                'total_seats': 30,
                'booked_seats': 0,
                'version': 0
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully seeded event with id 1'))
        else:
            # Ensure it has 30 seats if it already exists
            event.total_seats = 30
            event.booked_seats = 0
            event.version = 0
            event.save()
            self.stdout.write(self.style.SUCCESS('Event with id 1 already exists, reset to 30 seats'))
