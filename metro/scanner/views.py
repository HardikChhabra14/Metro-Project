from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta

from tickets.models import Ticket
from stations.models import Station
from .models import ScanLog, StationFootfall


def is_scanner(user):
    return user.groups.filter(name='Scanner').exists()


@login_required
@user_passes_test(is_scanner)
def scan_ticket(request):
    message = ""

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        action = request.POST.get('action')  # entry / exit

        try:
            ticket = Ticket.objects.get(id=ticket_id)

            # --- Anti-fraud: scan order + time gap ---
            last_scan = ScanLog.objects.filter(ticket=ticket).order_by('-scanned_at').first()

            is_entry = action == 'entry'

            if last_scan:
                if last_scan.is_entry == is_entry:
                    return render(request, "scanner/error.html", {
                        "message": "Invalid scan sequence"
                    })

                if timezone.now() - last_scan.scanned_at < timedelta(minutes=1):
                    return render(request, "scanner/error.html", {
                        "message": "Scan too fast"
                    })

            # --- ENTRY ---
            if action == 'entry' and ticket.status == 'ACTIVE':
                ticket.status = 'IN_USE'
                ticket.save()

                footfall, _ = StationFootfall.objects.get_or_create(
                    station=ticket.source,
                    date=timezone.now().date()
                )
                footfall.entry_count += 1
                footfall.save()

                ScanLog.objects.create(ticket=ticket, is_entry=True)
                message = "Entry scan successful"

            # --- EXIT ---
            elif action == 'exit' and ticket.status == 'IN_USE':
                ticket.status = 'USED'
                ticket.save()

                footfall, _ = StationFootfall.objects.get_or_create(
                    station=ticket.destination,
                    date=timezone.now().date()
                )
                footfall.exit_count += 1
                footfall.save()

                ScanLog.objects.create(ticket=ticket, is_entry=False)
                message = "Exit scan successful"

            else:
                message = "Invalid scan"

        except Ticket.DoesNotExist:
            message = "Ticket not found"

    return render(request, 'scanner/scan.html', {'message': message})


@login_required
@user_passes_test(is_scanner)
def offline_ticket(request):
    message = ""
    stations = Station.objects.all().order_by('order')

    if request.method == 'POST':
        source_id = request.POST.get('source')
        destination_id = request.POST.get('destination')
        price = request.POST.get('price')

        source = Station.objects.get(id=source_id)
        destination = Station.objects.get(id=destination_id)

        Ticket.objects.create(
            passenger=None,
            source=source,
            destination=destination,
            price=price,
            status='USED'
        )

        message = "Offline ticket created and marked as USED"

    return render(request, 'scanner/offline.html', {
        'stations': stations,
        'message': message
    })
