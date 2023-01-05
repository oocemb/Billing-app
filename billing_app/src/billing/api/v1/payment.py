from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from billing.view_models import PurchaseIn
from billing.service.payment_service import PaymentService
from billing.core.errors import ErrorStatus

router = APIRouter()


@router.post("/create/", summary="Create new payment")
async def pay_create(payment: PurchaseIn) -> str:
    url = await PaymentService.create_new_payment(payment)

    if not url:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=ErrorStatus.ITEMS_NOT_FOUND
        )

    return url


@router.post("/create_recurrent/", summary="Create new recurrent payment")
async def pay_create_recurrent():
    await PaymentService.recurrent_batch()
    return "OK"


@router.get("/{payment_id}/status/", summary="get payment status")
async def pay_status(payment_id: int):
    # provider = get_payment_provider(payment.payment_method)
    # status = provider.check_status(payment.id)
    # return status
    return "OK"


@router.post("/check_missed_callback_payments/", summary="Check missed callback payments")
async def check_missed_callback_payments():
    # Делаем выборку пачки платежей в статусе CREATED
    # для каждого платежа проводим запрос к его провайдеру за текущим статусом
    # Если всё ок, переставляем статус платежа на Успешный и ЕТЛ синхронизирует данные в фронт
    # Если не ок, переставляем статус на "Конкретную Ошибку"
    # или
    # Если ещё идёт обработка (пользователь тупит) ничего не делаем
    return "OK"
