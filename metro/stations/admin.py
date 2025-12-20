# Register your models here.
from django.contrib import admin
from .models import MetroLine, Station

admin.site.register(MetroLine)
admin.site.register(Station)
