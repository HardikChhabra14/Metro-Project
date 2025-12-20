from django.db import models
from stations.models import Station
from django.utils import timezone


class ScanLog(models.Model):
    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE
    )
    scanned_at = models.DateTimeField(auto_now_add=True)
    is_entry = models.BooleanField()

    def __str__(self):
        return f"{self.ticket.id} - {self.station.name}"


class StationFootfall(models.Model):
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE
    )
    date = models.DateField(default=timezone.now)
    entry_count = models.PositiveIntegerField(default=0)
    exit_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("station", "date")

    def __str__(self):
        return f"{self.station.name} ({self.date})"


# Create your models here.
