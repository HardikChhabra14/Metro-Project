from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from stations.models import Station
from accounts.models import PassengerProfile
from .models import Ticket
from .utils import calculate_fare


from django.core.mail import send_mail
from .models import TicketOTP

@login_required
def buy_ticket(request):
    stations = Station.objects.all().order_by('order')
    error = ""

    if request.method == 'POST':
        source_id = request.POST.get('source')
        destination_id = request.POST.get('destination')

        if source_id == destination_id:
            error = "Source and destination cannot be the same."
        else:
            source = Station.objects.get(id=source_id)
            destination = Station.objects.get(id=destination_id)
            fare = calculate_fare(source, destination)

            profile, _ = PassengerProfile.objects.get_or_create(user=request.user)

            if profile.wallet_balance < fare:
                error = "Insufficient wallet balance"
            else:
                otp_code = TicketOTP.generate_otp()
                TicketOTP.objects.create(user=request.user, otp=otp_code)

                send_mail(
                    'Metro Ticket OTP',
                    f'Your OTP for ticket purchase is {otp_code}. It expires in 5 minutes.',
                    None,
                    [request.user.email],
                )

                request.session['ticket_data'] = {
                    'source': source.id,
                    'destination': destination.id,
                    'fare': fare
                }

                return redirect('verify_otp')

    return render(request, 'tickets/buy_ticket.html', {
        'stations': stations,
        'error': error
    })
@login_required
def verify_otp(request):
    error = ""

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        try:
            otp_obj = TicketOTP.objects.filter(
                user=request.user,
                otp=entered_otp,
                is_verified=False
            ).latest('created_at')

            if otp_obj.is_expired():
                error = "OTP expired"
            else:
                otp_obj.is_verified = True
                otp_obj.save()

                data = request.session.get('ticket_data')
                source = Station.objects.get(id=data['source'])
                destination = Station.objects.get(id=data['destination'])
                fare = data['fare']

                profile = PassengerProfile.objects.get(user=request.user)
                profile.wallet_balance -= fare
                profile.save()
                from stations.utils import calculate_ticket_price

                Ticket.objects.create(
                    passenger=request.user,
                    source=source,
                    destination=destination,
                    price=fare,
                    status='ACTIVE',
                )

                del request.session['ticket_data']
                return redirect('ticket_success')

        except TicketOTP.DoesNotExist:
            error = "Invalid OTP"

    return render(request, 'tickets/verify_otp.html', {'error': error})

# Create your views here.

from django.contrib.auth.decorators import login_required

@login_required
def ticket_history(request):
    tickets = Ticket.objects.filter(passenger=request.user).order_by('-created_at')
    return render(request, 'tickets/history.html', {'tickets': tickets})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def ticket_success(request):
    ticket = Ticket.objects.filter(passenger=request.user).latest('created_at')
    return render(request, 'tickets/ticket_success.html', {'ticket': ticket})
