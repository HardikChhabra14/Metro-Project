# Create your models here.
from django.db import models

class MetroLine(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    ticket_purchase_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MetroLine(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    lines = models.ManyToManyField(MetroLine, related_name='stations')

    def __str__(self):
        return self.name