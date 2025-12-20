from django.urls import path
from .views import scan_ticket, offline_ticket

urlpatterns = [
    path('scan/', scan_ticket, name='scan_ticket'),
    path('offline/', offline_ticket, name='offline_ticket'),
]
