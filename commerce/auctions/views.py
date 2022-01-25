from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from .forms import ListingForm


def index(request: HttpRequest) -> HttpResponse:
    """Renders the index view with all active listings."""
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        'listings': listings
    })


def login_view(request: HttpRequest) -> HttpResponse:
    """Logs the user in."""
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request: HttpRequest) -> HttpResponse:
    """Logs the user out."""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request: HttpRequest) -> HttpResponse:
    """Registers a new user."""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def create(request: HttpRequest) -> HttpResponse:
    """Allows users to create a new listing."""

    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        form = ListingForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = user
            listing.current_bid = listing.starting_bid
            listing.save()

            return HttpResponseRedirect(reverse('index'))

    else:
        form = ListingForm()

    return render(request, 'auctions/create.html', {
        'form': form
    })
