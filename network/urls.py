
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path("all_post", views.all_post_view, name="all_post"),
    path("profile/<str:name>", views.show_profile, name="profile"),
    path("following", views.show_following, name="following")
]
