from django.urls import path
from . import views


urlpatterns = [
    path("", views.polls, name="Polls"),
    path("register", views.register, name="Register"),
    path("login", views.login, name="Login"),
    path("logout", views.logout, name="Logout"),
    path("add_poll", views.add_poll, name="Add Poll"),
    path("add_poll_process", views.add_poll_process, name="Add Poll Process"),
    path("my_poll", views.my_polls, name="My Polls"),
    path("search", views.search, name="Search"),
    path("vote/<int:poll_id>", views.vote, name="Vote"),
    path("result_map", views.result_map, name="Result map"),
    path("result/<int:poll_id>", views.result, name="Result"),
    path("profile/<int:user_id>", views.profile, name="Profile"),
    path("follow/<int:followed_id>/<int:follower_id>", views.follow, name="Follow"),
    path("unfollow/<int:followed_id>/<int:follower_id>", views.unfollow, name="Unfollow"),
    path("discover", views.discover, name="Discover"),


]
