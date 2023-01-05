from django.urls import path
from .views import user_info, movie_info
from .callback_view import callback, success, fail

urlpatterns = [
    path("user/<pk>/", user_info, name="user_info"),
    path("movie/<pk>/", movie_info, name="movie_info"),
    path("<provider>/callback", callback, name="callback"),
    path("<provider>/success", success, name="success"),
    path("<provider>/fail", fail, name="fail"),
]
