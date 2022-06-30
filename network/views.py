from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile
import operator
from django.core.paginator import Paginator
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json


post_paginator = None 
post_per_page = 2
page_now = 1

class NewPostForm(forms.Form):
    words = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'round text-light bg-dark border-primary'}))


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
    posts = Post.objects.order_by("-post_time").all()
    global post_paginator
    global page_now
    post_paginator = Paginator(posts, post_per_page)
    page_now = 1
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        return render(request, 'network/all_post.html', {
            "user_info": Profile.objects.get(owner=current_user),
            "posts": post_paginator.page(1),
            "new_post_form": NewPostForm(),
            "name": request.user,
            "index": True,
        })
    else:
        return render(request, 'network/all_post.html', {
            "posts": post_paginator.page(1),
            "index": True,
        })

def show_profile(request, name):
    print("show_profile", name)
    # haven't fix the problem that others can peak your profile
    current_user = User.objects.get(username=name)
    global post_paginator
    global page_now
    post_paginator = Paginator(Post.objects.filter(poster=current_user).order_by("-post_time").all(), post_per_page)
    page_now = 1
    for post in post_paginator.page(1):
        print(type(post))
    for tmp in Profile.objects.get(owner=current_user).like_post.all():
        print(tmp)
    # print("!!!!", Profile.objects.get(owner=current_user))
    return render(request, 'network/all_post.html', {
        "user_info": Profile.objects.get(owner=current_user),  
        "posts": post_paginator.page(1),
        "new_post_form": NewPostForm(),
        "name": request.user,
        "show_info": True,
    })

def show_following(request):
    current_user = User.objects.get(username=request.user)
    follow_to_list = Profile.objects.get(owner=current_user).follow_to.all()
    global post_paginator
    global page_now
    # print(not follow_to_list)
    if not follow_to_list:
        post_paginator = Paginator([], post_per_page)
        page_now = 1
        return render(request, 'network/all_post.html', {
            "message": "You are not following someone."
        })
    post_lists = []
    for follow_to in follow_to_list:
        tmp_set = Post.objects.filter(poster=follow_to)
        for tmp in tmp_set:
            post_lists.append(tmp)
    print(post_lists)
    ordered = sorted(post_lists, key=operator.attrgetter('post_time'), reverse=True)
    print(post_lists)
    
    post_paginator = Paginator(ordered, post_per_page)
    page_now = 1
    return render(request, 'network/all_post.html', {
        "user_info": Profile.objects.get(owner=current_user),
        "posts": post_paginator.page(1),
        "new_post_form": NewPostForm(),
        "name": request.user,
    })

def turn_next(request):
    print("turn next")
    global page_now
    print("page_now", page_now)
    if page_now+1 <= post_paginator.num_pages:
        page_now = page_now + 1
        print("plus ", page_now)
        next_page = post_paginator.page(page_now)
        return JsonResponse([post.serialize(request.user) for post in next_page], safe=False)
    else:
        return JsonResponse({"error": "Page out of range.",}, status=400)

def turn_prev(request):
    print("turn prev")
    global page_now
    print("page_now", page_now)
    if page_now-1 >= 1:
        page_now = page_now - 1
        print("minus ", page_now)
        prev_page = post_paginator.page(page_now)
        print("okay", [post.serialize(request.user) for post in prev_page])
        return JsonResponse([post.serialize(request.user) for post in prev_page], safe=False)
    else:
        return JsonResponse({"error": "Page out of range.",}, status=400)

def check_has_another(request):
    # print("check has another")
    # print("count", post_paginator.count)
    has_next = True
    has_prev = True
    # print("page_now vs num_pages", page_now, post_paginator.num_pages)
    if page_now == post_paginator.num_pages:
        has_next = False
    if page_now == 1:
        has_prev = False
    # print(has_prev, has_next)
    page_info = {
        "has_next": has_next,
        "has_prev": has_prev,
    }
    # print("page_info", page_info)
    # print("check here")
    return JsonResponse(page_info, status=200)

def store_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            ct = form.cleaned_data["words"]
            current_user = User.objects.get(username=request.user)
            new_post = Post(poster=current_user, content=ct, like_num=0)
            new_post.save()
    return HttpResponseRedirect(reverse("index"))
        # data = json.loads(request.body)
        # if not data.get("content"):
        #     return JsonResponse({
        #         "msg": "Content should not be empty."
        #     }, status=400)
        # new_post = Post(poster=request.user, content=data.get("content_of_post"), like_num=0)
        # new_post.save()
        # return JsonResponse({
        #     "msg": "ok"
        # }, status=200)

@csrf_exempt
def like_motion(request):
    data = json.loads(request.body)
    cur_post = Post.objects.get(id=data["now_id"])
    print(cur_post)
    in_list = False
    for fan in cur_post.like_list.all():
        if request.user == fan.owner:
            in_list = True
            break
    if in_list:
        print("remove from list")
        Profile.objects.get(owner=request.user).like_post.remove(cur_post)
        cur_post.like_num -= 1
    else :
        print("add to list")
        Profile.objects.get(owner=request.user).like_post.add(cur_post)
        cur_post.like_num += 1
    cur_post.save()
    return JsonResponse({"msg": "successful"})