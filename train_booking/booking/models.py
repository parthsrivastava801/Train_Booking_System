from django.db import models
from django.conf import settings

class Train(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    seats_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.source} -> {self.destination})"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    booking_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} on {self.train.name} (Seat {self.seat_number})"
