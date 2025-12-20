# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from scanner.models import StationFootfall

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def footfall_dashboard(request):
    footfalls = StationFootfall.objects.all().order_by('-date')
    return render(request, 'admin_dashboard/footfall.html', {
        'footfalls': footfalls
    })
