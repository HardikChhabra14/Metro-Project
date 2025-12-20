from django.urls import path
from .views import buy_ticket, ticket_history, verify_otp, ticket_success



urlpatterns = [
    path('buy/', buy_ticket, name='buy_ticket'),
    path('success/', ticket_success, name='ticket_success'),
    path('history/', ticket_history, name='ticket_history'),
    path('verify-otp/', verify_otp, name='verify_otp'),

]


