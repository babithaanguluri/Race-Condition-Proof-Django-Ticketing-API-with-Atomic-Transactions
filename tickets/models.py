from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    total_seats = models.IntegerField()
    booked_seats = models.IntegerField(default=0)
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.event.name}"
