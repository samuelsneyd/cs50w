from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'hello/user.html')


def samuel(request):
    return HttpResponse('Hello, Samuel!')


def greet(request, name: str):
    return render(request, 'hello/greet.html', {
        'name': name.capitalize()
    })

