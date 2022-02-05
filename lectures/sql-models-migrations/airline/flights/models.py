from django.db import models


# Create your models here
class Airport(models.Model):
    """
    Airports class.
    """

    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    """
    Flights class.
    """

    origin = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departures"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrivals"
    )
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.pk}: {self.origin} to {self.destination}"


class Passenger(models.Model):
    """
    Passengers class.
    """

    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"
