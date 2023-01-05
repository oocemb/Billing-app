from django.urls import path
from .views import (
    home,
    my_movies,
    movie_detail,
    subscribe_plans,
    payment_gate,
    movie_player,
    user_payment_history,
    subs_cancel,
    user_profile,
    user_subscription,
)
from .views import redirect_view

# app_name = "front"
urlpatterns = [
    path("", home, name="home"),
    path("my_movies/", my_movies, name="my_movies"),
    path("movie/<uuid>/", movie_detail, name="movie_detail"),
    path("player/<uuid>/", movie_player, name="movie_player"),
    path("subscribe_plans/", subscribe_plans, name="subscribe_plans"),
    path("payment_gate/", payment_gate, name="payment_gate"),
    path("history_payments/", user_payment_history, name="user_payment_history"),
    path("user_subscription/", user_subscription, name="user_subscription"),
    path("user_profile/", user_profile, name="user_profile"),
    path("redirect_to_gate_url/", redirect_view, name="redirect_to_gate_url"),
    path("subs_cancel/", subs_cancel, name="subs_cancel"),
]
