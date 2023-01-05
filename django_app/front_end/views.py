import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.db.models import Count

from .models import Product, PlanSubscriptionMovie, PurchasedMovies
from my_auth.models import Profile
from .utils import (
    paginator_create,
    get_redirect_url_in_billing_service,
    get_user_payment_history_in_billing_service,
    cancel_user_subs_in_billing_service
)


def home(request):
    """Генерирует основную главную страницу сайта"""
    # TODO: можно добавить отдельно флаг в модель в продвигаемые продукты
    featured_products = Product.objects.filter(is_active=True)
    # Вытаскивает все категории с их картинкой (если потребуется потом) и считает количество фильмов в каждой их них
    categories_with_count = (
        Product.objects.values("category__name", "category__image")
        .filter(is_active=True)
        .annotate(count=Count("id"))
    )
    _ITEM_PER_PAGE = 8
    is_paginated, prev_url, next_url, current_page = paginator_create(
        featured_products, _ITEM_PER_PAGE, request
    )
    return render(
        request,
        "home.html",
        context={
            "is_paginated": is_paginated,
            "next_url": next_url,
            "prev_url": prev_url,
            "featured_products": current_page,
            "categories_count": categories_with_count,
        },
    )


@login_required
def my_movies(request):
    purchased_movies_ids = list(PurchasedMovies.objects.filter(user=request.user).values_list('movie_id__pk', flat=True))
    purchased_movies = Product.objects.filter(pk__in=purchased_movies_ids)
    # Вытаскивает все категории с их картинкой (если потребуется потом) и считает количество фильмов в каждой их них
    categories_with_count = (
        Product.objects.values("category__name", "category__image")
        .filter(is_active=True)
        .annotate(count=Count("id"))
    )
    _ITEM_PER_PAGE = 8
    is_paginated, prev_url, next_url, current_page = paginator_create(
        purchased_movies, _ITEM_PER_PAGE, request
    )

    return render(
        request,
        "home.html",
        context={
            "is_paginated": is_paginated,
            "next_url": next_url,
            "prev_url": prev_url,
            "featured_products": current_page,
            "categories_count": categories_with_count,
        },
    )


def subscribe_plans(request):
    subs = PlanSubscriptionMovie.objects.all()
    return render(request, "subscribe_plans.html", locals())


@login_required
def user_subscription(request):
    date_pay = request.user.profile.subscription_last_payment_date
    if date_pay:
        date_now = datetime.date.today()
        day_new_recurrent = date_pay - date_now + datetime.timedelta(days=30)
        day_new_recurrent = day_new_recurrent.days
    else:
        day_new_recurrent = 0
    return render(request, "user-subscription.html", locals())


@login_required
def user_profile(request):
    return render(request, "user-profile.html", locals())


@login_required
def user_payment_history(request):
    payments = get_user_payment_history_in_billing_service(request.user.profile.uuid)
    product_purchased = []
    for payment in payments:
        if payment.product_type == "subs":
            title_class = PlanSubscriptionMovie.objects.get(uuid=payment.product_id)
        else:  # payment.product_type == 'buy':
            title_class = Product.objects.get(uuid=payment.product_id)
        payment.title = title_class.name
    return render(request, "user-payment-history.html", locals())


@login_required
def subs_cancel(request):
    ## Block post request in billing
    if cancel_user_subs_in_billing_service(request.user.profile.uuid):
    ## Block change front (auth) db
        profile = Profile.objects.get(user=request.user)
        profile.subscription_status = "cancel"
        profile.save()
        return redirect(reverse('front_end:user_subscription'))
    else:
        return redirect(reverse('front_end:user_subscription'))


@login_required
def payment_gate(request):
    if request.method == "POST":
        coupon = request.POST.get("coupon")
        paymethod = request.POST.get("paymethod")
        product_type = request.POST.get("product_type")
        content = request.POST.get("content")
        if product_type == "buy":
            purchased_from_url = request.POST.get("purchased_from_url")
        else:
            purchased_from_url = "/"
        return redirect(
            f"/redirect_to_gate_url/"
            f"?coupon={coupon}&paymethod={paymethod}&product_type={product_type}"
            f"&content={content}&purchased_from_url={purchased_from_url}"
        )
    elif request.method == "GET":
        product_type = request.GET["product_type"]
        if product_type == "subs":
            content = request.GET["subs_plan"]
        elif product_type == "buy":
            content = request.GET["movie_id"]
            purchased_from_url = request.GET["purchased_from_url"]

    return render(request, "payment-gate2.html", locals())


def movie_detail(request, uuid):
    product = Product.objects.get(uuid=uuid)
    return render(request, "movie_detail.html", locals())


@login_required
def movie_player(request, uuid):
    product = Product.objects.get(uuid=uuid)
    return render(request, "movie-player.html", locals())


@login_required
def redirect_view(request):
    product_type = request.GET["product_type"]
    if product_type == "subs":
        _ = PlanSubscriptionMovie.objects.get(uuid=request.GET["content"])
        price = str(_.price)
    elif product_type == "buy":
        _ = Product.objects.get(uuid=request.GET["content"])
        price = str(_.price_tier.price)
    else:
        price = "999999"  # run exception
    payload = {
        "user_id": str(request.user.profile.uuid),
        "payment_type": request.GET["product_type"],
        "content": request.GET["content"],
        "coupon": request.GET["coupon"],
        "price": price,
        "is_recurrent": True,
        "payment_provider": request.GET["paymethod"],
        "purchased_from_url": request.GET["purchased_from_url"],
    }
    url = get_redirect_url_in_billing_service(payload)
    # TODO: custom exception
    if url == "Gate process error":
        msg = "Gate process error"
        return render(request, "message.html", locals())
    elif url == "Connection to billing error":
        msg = "Connection to billing error"
        return render(request, "message.html", locals())
    elif url:
        return HttpResponseRedirect(url)
    else:
        msg = "Unknown Error"
        return render(request, "message.html", locals())
