from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by("created_at").reverse()

    return render(request, "network/index.html", {
        "posts": posts,
        "title": "All Posts"
    })


@login_required
def following(request):
    if request.user.following.count() > 0:
        posts = Post.objects.filter(user__in=request.user.following)
    else:
        posts = None

    return render(request, "network/index.html", {
        "posts": posts,
        "title": "Followed Posts"
    })


def login_view(request):
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        text = request.POST["text"]
        try:
            post = Post(
                user=request.user,
                text=text
            )
            post.save()
        except IntegrityError:
            return redirect(reverse("index"), {"message": "Error when creating new post"})

    return redirect(reverse("index"))


def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    return render(request, "network/user.html", {"user": user})
