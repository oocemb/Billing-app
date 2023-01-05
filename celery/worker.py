import os
import logging

from celery import Celery, shared_task
from celery.schedules import crontab
import requests

logger = logging.getLogger()

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
celery.conf.beat_schedule = {
    "check_and_create_new_recurrent_payments_batch": {
        "task": "check_and_create_new_recurrent_payments_batch",
        # 'schedule': crontab(minute=0, hour='0,3,6,9,12,15,18,21'),  # Every 3 hour run new batch
        "schedule": 180,  # test run
    },
    # todo: Если платёж уже обработан сегодня дважды его не пытаться провести а новую попытку делать только завтра \
    #  счётчик попыток корректно обработать
    "sync_data_in_django_and_billing": {
        "task": "sync_data_in_django_and_billing",
        # 'schedule': crontab(hour=2, minute=30),  # Every night run sync ETL process
        "schedule": 140,  # test run
    },
    "check_missed_callback_payments": {
        "task": "check_missed_callback_payments",
        "schedule": 120,  # Every 2 minute run
    },
}

BILLING_API_NEW_RECURRENT_PAYMENT_URL = (
    "http://127.0.0.1:5000/api/v1/payment/create_recurrent/"
)
BILLING_API_CHECK_MISSED_PAYMENTS_URL = (
        "http://127.0.0.1:5000/api/v1/payment/check_missed_callback_payments/"
)


@shared_task(name="check_and_create_new_recurrent_payments_batch")
def check_and_create_new_recurrent_payments_batch():
    logger.info("check_and_create_new_recurrent_payments_batch run")
    header = {"Token": "Celery-bro"}
    requests.post(url=BILLING_API_NEW_RECURRENT_PAYMENT_URL, headers=header)


@shared_task(name="sync_data_in_django_and_billing")
def sync_data_in_django_and_billing():
    logger.info("sync_data_in_django_and_billing run")
    # from etl import sync_data
    # sync_data()


@shared_task(name="check_missed_callback_payments")
def check_missed_callback_payments():
    logger.info("check_missed_callback_payments run")
    header = {"Token": "Celery-bro"}
    requests.post(url=BILLING_API_CHECK_MISSED_PAYMENTS_URL, headers=header)
