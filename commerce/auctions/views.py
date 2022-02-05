from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category
from .forms import ListingForm, CommentForm


def index(request: HttpRequest) -> HttpResponse:
    """Renders the index view with all active listings."""
    listings = Listing.objects.all()

    return render(
        request,
        "auctions/index.html",
        {"listings": listings},
    )


def login_view(request: HttpRequest) -> HttpResponse:
    """Logs the user in and redirects to index on login."""
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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )

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
            return render(
                request,
                "auctions/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/register.html")


@login_required(login_url="login")
def create(request: HttpRequest) -> HttpResponse:
    """Allows users to create a new listing."""

    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk)
        create_listing_form = ListingForm(request.POST)

        if create_listing_form.is_valid():
            listing = create_listing_form.save(commit=False)
            listing.user = user
            listing.current_bid = listing.starting_bid
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=[listing.pk]))

    else:
        create_listing_form = ListingForm()

    return render(
        request,
        "auctions/create.html",
        {"create_listing_form": create_listing_form},
    )


def listing_page(request: HttpRequest, listing_id: int) -> HttpResponse:
    """Page for individual listings."""
    try:
        listing = Listing.objects.get(pk=listing_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    comment_form = CommentForm()
    comments = listing.comments.all()
    is_watching = False
    user = None

    if request.user:
        user = User.objects.get(pk=request.user.pk)
        if len(user.watching.filter(pk=listing_id)) > 0:
            is_watching = True

    return render(
        request,
        "auctions/listing.html",
        {
            "user": user,
            "listing": listing,
            "comments": comments,
            "comment_form": comment_form,
            "is_watching": is_watching,
        },
    )


@login_required(login_url="login")
def watch(request: HttpRequest) -> HttpResponse:
    """Add or remove listings from watchlist"""
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=request.POST.get("pk"))

        if user not in listing.watchers.all():
            listing.watchers.add(user)
        else:
            listing.watchers.remove(user)

        return HttpResponseRedirect(reverse("listing", args=[listing.pk]))

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def watchlist(request: HttpRequest) -> HttpResponse:
    """Displays the users watched listings."""
    listings = request.user.watching.all()

    return render(
        request,
        "auctions/watchlist.html",
        {"listings": listings},
    )


def comment(request: HttpRequest, listing_id: int) -> HttpResponse:
    """Handles adding a comment to a listing."""
    try:
        listing = Listing.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    comment_form = CommentForm(request.POST)

    if listing is not None and comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = user
        new_comment.listing = listing
        new_comment.save()

    return HttpResponseRedirect(reverse("listing", args=[listing.pk]))


def bid(request: HttpRequest, listing_id) -> HttpResponse:
    """Handles users bidding on a listing."""
    return HttpResponse("TODO")


def categories(request: HttpRequest) -> HttpResponse:
    """Renders a page with links to all listing categories."""
    category_list = Category.objects.all()
    return render(
        request,
        "auctions/categories.html",
        {"categories": category_list},
    )


def category(request: HttpRequest, category_name: str) -> HttpResponse:
    """Renders a page with all listings of a particular category."""
    try:
        current_category = Category.objects.get(name=category_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("categories"))

    listings = Listing.objects.filter(category=current_category)

    return render(
        request,
        "auctions/category.html",
        {
            "category": current_category,
            "listings": listings,
        },
    )
