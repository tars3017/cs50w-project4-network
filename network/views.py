from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile


def index(request):
    return render(request, "network/index.html")


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

            profile = Profile(owner=user)
            profile.save()
        except IntegrityError:
            print(username, email, password, IntegrityError)
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def index(request):
    if request.method == "POST":
        TODO
    posts = Post.objects.order_by("post_time").all()
    return render(request, 'network/all_post.html', {
        "posts": posts
    })

def show_profile(request, name):
    current_user = User.objects.get(username=name)
    print("!!!!", Profile.objects.get(owner=current_user))
    return render(request, 'network/profile.html', {
        "user_info": Profile.objects.get(owner=current_user),  
        "my_posts": Post.objects.filter(poster=current_user).all()
    })

def show_following(request):
    current_user = User.objects.get(username=request.name)
    # following_post = Post.objects.