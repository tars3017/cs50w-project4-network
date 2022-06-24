from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile
import operator
from django.core.paginator import Paginator
from django.http import JsonResponse


post_paginator = None 
post_per_page = 2
page_now = 1

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
    posts = Post.objects.order_by("-post_time").all()
    global post_paginator
    global page_now
    post_paginator = Paginator(posts, post_per_page)
    page_now = 1
    # print(post_paginator)
    return render(request, 'network/all_post.html', {
        "posts": post_paginator.page(1)
    })

def show_profile(request, name):
    current_user = User.objects.get(username=name)
    global post_paginator
    global page_now
    post_paginator = Paginator(Post.objects.filter(poster=current_user).order_by("-post_time").all(), post_per_page)
    page_now = 1
    # print("!!!!", Profile.objects.get(owner=current_user))
    return render(request, 'network/profile.html', {
        "user_info": Profile.objects.get(owner=current_user),  
        "my_posts": post_paginator.page(1)
    })

def show_following(request):
    current_user = User.objects.get(username=request.user)
    follow_to_list = Profile.objects.get(owner=current_user).follow_to.all()
    post_lists = []
    for follow_to in follow_to_list:
        tmp_set = Post.objects.filter(poster=follow_to)
        for tmp in tmp_set:
            post_lists.append(tmp)
    print(post_lists)
    ordered = sorted(post_lists, key=operator.attrgetter('post_time'), reverse=True)
    print(post_lists)
    global post_paginator
    global page_now
    post_paginator = Paginator(ordered, post_per_page)
    page_now = 1
    return render(request, 'network/all_post.html', {
        "posts": post_paginator.page(1)
    })

def turn_next(request):
    print(post_paginator)
    global page_now
    if page_now+1 <= post_paginator.num_pages:
        page_now = page_now + 1
        next_page = post_paginator.page(page_now)
        print("okay", JsonResponse([post.serialize() for post in next_page], safe=False))
        return JsonResponse([post.serialize() for post in next_page], safe=False)
    else:
        return JsonResponse({"error": "Page out of range."}, status=400)
# def get_posts(request, target, page_idx):
#     if target == 'index':
#         if page_idx == 1:
#             posts = Post.objects.order_by("-post_time").all()
#             post_paginator = Paginator(posts, post_per_page)
#             return JsonResponse([post.serialize() for post in post_paginator.page(1)], safe=False)
#         elif page_idx <= post_paginator.num_pages:
#             return JsonResponse([post.serialize() for post in post_paginator.page(page_idx)], safe=False)
#             # [email.serialize() for email in emails], safe=False
#         else:
#             return JsonResponse({"error": "Page out of range."}, status=400)

#     elif target == 'following':
#         if page_idx == 1:
#             current_user = User.objects.get(username=request.user)
#             follow_to_list = Profile.objects.get(owner=current_user).follow_to.all()
#             post_lists = []
#             for follow_to in follow_to_list:
#                 tmp_set = Post.objects.filter(poster=follow_to)
#                 for tmp in tmp_set:
#                     post_lists.append(tmp)
#             ordered = sorted(post_lists, key=operator.attrgetter('post_time'), reverse=True)
#             post_paginator = Paginator(ordered, post_per_page)
#             return JsonResponse([post.serialize() for post in post_paginator.page(1)], safe=False)
        
#         elif page_idx <= post_paginator.num_pages:
#             return JsonResponse([post.serialize() for post in post_paginator.page(page_idx)], safe=False)
        
#         else:
#             return JsonResponse({"error": "Page out of range."}, status=400)
    
#     else: # personal post
#         if page_idx == 1:
#             current_user = User.objects.get(username=name)
#             post_paginator = Paginator(Post.objects.filter(poster=current_user).order_by("-post_time").all(), post_per_page)
#             return JsonResponse([post.serialize() for post in post_paginator.page(1)], safe=False)
        
#         elif page_idx <= post_paginator.num_pages:
#             return JsonResponse([post.serialize() for post in post_paginator.page(page_idx)], safe=False)
    
#         else:
#             return JsonResponse({"error": "Page out of range."}, status=400)
    

# def show_personal_info(request):
#     current_user = User.objects.get(username=request.username)
#     return_data = Profile.objects.get(owner=current_user)
#     return JsonResponse(return_data.serialize(), safe=False)