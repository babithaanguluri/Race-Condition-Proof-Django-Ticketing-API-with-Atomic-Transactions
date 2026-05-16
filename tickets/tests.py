from django.test import TestCase
from .models import Event, Booking

class BookingModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            total_seats=10,
            booked_seats=0
        )

    def test_event_creation(self):
        """Events are created correctly with initial values."""
        self.assertEqual(self.event.name, "Test Event")
        self.assertEqual(self.event.total_seats, 10)
        self.assertEqual(self.event.booked_seats, 0)

    def test_booking_creation(self):
        """Bookings are correctly linked to events."""
        booking = Booking.objects.create(
            event=self.event,
            user_name="test_user"
        )
        self.assertEqual(booking.event, self.event)
        self.assertEqual(booking.user_name, "test_user")
