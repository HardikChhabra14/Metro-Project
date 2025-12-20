from django.db import models
from django.contrib.auth.models import User
from stations.models import Station

class Ticket(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='source_tickets')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_tickets')
    price = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

import random


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class TicketOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp():
        return str(random.randint(100000, 999999))
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"


# Create your models here.

