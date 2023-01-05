from .models import PurchasedMovies


def getting_purchased_movies(request):
    pur_mov_uuids = []
    purchased_movies = PurchasedMovies.objects.filter(user__pk=request.user.pk)
    for mov in purchased_movies:
        pur_mov_uuids.append(mov.movie_id.uuid)
    return locals()
