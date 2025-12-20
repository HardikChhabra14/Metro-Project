# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    message = ""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            message = "Invalid credentials"

    return render(request, 'accounts/login.html', {'message': message})


def logout_view(request):
    logout(request)
    return redirect('/login/')
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def home(request):
    if request.user.groups.filter(name='Scanner').exists():
        return redirect('/scanner/scan/')
    else:
        return redirect('/tickets/buy/')
