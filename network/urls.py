
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path("all_post", views.all_post_view, name="all_post"),
    path("profile/<str:name>", views.show_profile, name="profile"),
    path("following", views.show_following, name="following"),
    path("next", views.turn_next, name="next"),
    path("prev", views.turn_prev, name="prev"),
    path("has_another", views.check_has_another, name="another"),
    path("send_post", views.store_post, name="send"),
    path("like_unlike", views.like_motion, name="like"),
    path("change_post", views.change_ct, name="change_post"),
    # path("prev", views.turn_prev, name="prev"),
]
