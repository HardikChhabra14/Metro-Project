# Register your models here.
from django.contrib import admin
from .models import ScanLog, StationFootfall

@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ("ticket", "station", "is_entry", "scanned_at")
    list_filter = ("station", "is_entry")
    search_fields = ("ticket__id",)


@admin.register(StationFootfall)
class StationFootfallAdmin(admin.ModelAdmin):
    list_display = ("station", "date", "entry_count", "exit_count")
    list_filter = ("station", "date")
