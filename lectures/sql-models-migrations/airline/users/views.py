from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'users/user.html')


def login_view(request):
    """Log in page and logic for handling logging in."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'users/login.html', {
                'message': 'Invalid credentials'
            })

    return render(request, 'users/login.html')


def logout_view(request):
    """Logs the user out."""
    logout(request)
    return render(request, 'users/login.html', {
        'message': 'Logged out'
    })
