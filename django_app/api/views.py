from django.http.response import JsonResponse
from django.contrib.auth.models import User
from front_end.models import PurchasedMovies, Product


def user_info(request, pk):
    # В модели пользователя мы не переопределяли pk и сейчас он просто int
    # Во всех множественных дальнейших запросах необходимо использовать "select_related('Profile')"
    # для уменьшения числа запросов к базе
    user = User.objects.get(pk=pk)
    purchased_movies = PurchasedMovies.objects.filter(user__pk=pk)
    movies_list = []
    for movie in purchased_movies:
        movies_list.append(movie.movie_id.pk)

    return JsonResponse(
        data={
            "email": user.email,
            "username": user.username,
            "subscription_plan": user.profile.subscription_plan,
            "subscription_last_payment_date": user.profile.subscription_last_payment_date,
            "purchased_movies": movies_list,
        }
    )


def movie_info(request, pk):
    movie = Product.objects.get(pk=pk)
    return JsonResponse(
        data={
            "name": movie.name,
            "is_active": movie.is_active,
            "subscription_plan": movie.subscription_plan.name,
            "price_tier": movie.price_tier.name,
        }
    )
