from django.core.paginator import Paginator
from django.conf import settings
import requests

from .models_input import PaymentHistory


def paginator_create(objects, item_per_page, request):
    """Создание пагинатора и необходимых для него ссылок *вперёд *назад"""
    paginator = Paginator(objects, item_per_page)  # http://127.0.0.1:8000/posts/?page=2
    page_number = request.GET.get(
        "page", 1
    )  # дефолтное значение если не нашёл в запросе этот параметр
    current_page = paginator.get_page(page_number)
    is_paginated = current_page.has_other_pages()
    if current_page.has_previous():
        prev_url = "?page={}".format(current_page.previous_page_number())
    else:
        prev_url = False
    if current_page.has_next():
        next_url = "?page={}".format(current_page.next_page_number())
    else:
        next_url = False
    return is_paginated, prev_url, next_url, current_page


def get_redirect_url_in_billing_service(payload) -> str:
    billing_url = settings.BILLING_CREATE_PAYMENT
    auth_header = {"Token": "Django-bro"}
    try:
        response = requests.post(billing_url, headers=auth_header, json=payload)
    except requests.exceptions.ConnectionError:
        return "Connection to billing error"
    if response.status_code == 200:
        url = response.text
        return url[1:-1]
    return "Gate process error"


def cancel_user_subs_in_billing_service(user_uuid) -> bool:
    api_url = settings.BILLING_CANCEL_SUBSCRIPTION
    auth_header = {"Token": "Django-bro"}
    api_url = api_url.replace("<user_id>", str(user_uuid))
    try:
        response = requests.put(api_url, headers=auth_header)
    except requests.exceptions.ConnectionError:
        return False  # "Connection to billing error"
    if response.status_code == 200:
        return True
    return False  # "Gate process error"


def get_user_payment_history_in_billing_service(user_uuid) -> list[PaymentHistory]:
    api_url = settings.BILLING_PAYMENT_HISTORY
    auth_header = {"Token": "Django-bro"}
    api_url = api_url.replace("<user_id>", str(user_uuid))
    try:
        response = requests.get(api_url, headers=auth_header)
    except requests.exceptions.ConnectionError:
        raise Exception
    if response.status_code == 200:
        json_payments = response.json()
        return [PaymentHistory(**payment) for payment in json_payments]
        # todo: custom exception
    return []
