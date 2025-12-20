from django.urls import path
from .views import footfall_dashboard

urlpatterns = [
    path('footfall/', footfall_dashboard, name='footfall_dashboard'),
]
