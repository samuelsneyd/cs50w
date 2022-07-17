import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Post, Like


def index(request):
    posts = Post.objects.all().order_by("created_at").reverse()

    return render(request, "network/index.html", {
        "posts": posts,
        "title": "All Posts"
    })


@login_required
def following_view(request):
    followed_users = User.objects.filter(followers=request.user)
    posts = Post.objects.filter(user__in=followed_users)

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


@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        text = json.loads(request.body)['text']

        try:
            post = Post.objects.get(user=request.user, pk=post_id)
            post.text = text
            post.save()
            return JsonResponse({"success": "post updated successfully"}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({"error": "invalid request"}, status=400)

    return JsonResponse({"error": "method must be POST"}, status=400)


def user_profile_view(request, username):
    """Renders a user's profile view."""
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist:
        user_profile = None

    if user_profile:
        posts = Post.objects.filter(user=user_profile).order_by("created_at").reverse()
    else:
        posts = []

    is_following = False
    if request.user and user_profile and request.user in user_profile.followers.all():
        is_following = True

    return render(request, "network/user.html", {
        "user_profile": user_profile,
        "posts": posts,
        "is_following": is_following
    })


@login_required
def like_view(request, post_id):
    """Creates a like representing a user liking a post"""
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "post is not valid"}, status=400)

    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return JsonResponse({"success": "post unliked successfully"})
    except Like.DoesNotExist:
        like = Like.objects.create(user=request.user, post=post)
        like.save()
        return JsonResponse({"success": "post liked successfully"})


@login_required
def follow_view(request, user_id):
    """Follows a user"""
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        user_profile = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "user is not valid"}, status=400)

    if request.user in user_profile.followers.all():
        user_profile.followers.remove(request.user)
        return JsonResponse({"success": "user unfollowed successfully"})
    else:
        user_profile.followers.add(request.user)
        return JsonResponse({"success": "user followed successfully"})
