import datetime
import json
from enum import Enum

from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from front_end.models import PlanSubscriptionMovie, PurchasedMovies, Product
from my_auth.models import Profile
from .utils import validate_params_in_billing_api


class PaymentType(str, Enum):
    BUY = "buy"
    RENT = "rent"
    SUBSCRIBE = "subs"


@csrf_exempt
def callback(request, provider):
    body = ""

    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)

    api_url = settings.BILLING_CALLBACK
    params = (request.get_full_path(),)  # /api/robo/callback?params=value
    data = validate_params_in_billing_api(api_url, params[0], provider, body)

    ### Block save to DB
    usr = Profile.objects.get(uuid=data.get("user_id"))
    if data.get("payment_type") == PaymentType.BUY:
        curr_mov = Product.objects.get(uuid=data.get("content"))
        pur_mov = PurchasedMovies.objects.create(user=usr.user, movie_id=curr_mov)
        pur_mov.save()
    elif data.get("payment_type") == PaymentType.SUBSCRIBE:
        subs_plan = PlanSubscriptionMovie.objects.get(uuid=data.get("content"))
        usr.subscription_plan = subs_plan
        usr.subscription_status = 'enable'
        usr.subscription_last_payment_date = datetime.datetime.utcnow()
        usr.save()
    ###
    return HttpResponse(status=200)


def success(request, provider):
    api_url = settings.BILLING_SUCCESS
    params = (request.get_full_path(),)  # /api/robo/success?params=value
    data = validate_params_in_billing_api(api_url, params[0], provider)

    ### Block save to DB
    usr = Profile.objects.get(user__pk=request.user.pk)
    if data.get("payment_type") == "buy":
        curr_mov = Product.objects.get(uuid=data.get("content"))
        pur_mov = PurchasedMovies.objects.create(user=request.user, movie_id=curr_mov)
        pur_mov.save()
    elif data.get("payment_type") == "subs":
        subs_plan = PlanSubscriptionMovie.objects.get(uuid=data.get("content"))
        usr.subscription_plan = subs_plan
        usr.subscription_status = 'enable'
        usr.subscription_last_payment_date = datetime.datetime.utcnow()
        usr.save()
    ###

    ### Block redirect to purchaised movie or home page
    return redirect(data.get("redirect_url"))


def fail(request, provider):
    """Не готовая функция. Требует доработки"""
    api_url = settings.BILLING_FAIL
    # params = (request.get_full_path(),)  # /api/robo/success?params=value
    # data = validate_params_in_billing_api(api_url, params, provider)
    return redirect(reverse("front_end:home"))
