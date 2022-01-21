from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger


def index(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page with a list of flights.
    """
    return render(request, 'flights/user.html', {
        'flights': Flight.objects.all()
    })


def flight_page(request: HttpRequest, flight_id: int) -> HttpResponse:
    """
    Renders a page with the information of a specific flight.
    """
    try:
        flight = Flight.objects.get(pk=flight_id)
    except:
        return HttpResponse('Could not find flight')
    return render(request, 'flights/flight.html', {
        'flight': flight,
        'passengers': flight.passengers.all(),
        'non_passengers': Passenger.objects.exclude(flights=flight).all()
    })


def book(request: HttpRequest, flight_id: int) -> HttpResponse:
    """
    Renders a page that allows users to add passengers to a flight.
    """
    if request.method == 'POST':
        try:
            flight = Flight.objects.get(pk=flight_id)
            passenger = Passenger.objects.get(pk=int(request.POST['passenger']))
        except:
            return HttpResponse('Could not find flight or passenger')

        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('flight', args=(flight.id,)))
