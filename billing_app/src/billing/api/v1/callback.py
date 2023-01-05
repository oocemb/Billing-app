from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from billing.service.payment_service import PaymentService
from billing.view_models import PaymentCallbackIn

router = APIRouter()


@router.post(
    "/{payment_gate}/callback/",
    summary="Post event message info",
    description="Post event message info",
)
async def gate_result(payload: PaymentCallbackIn, payment_gate: str):

    ret = await PaymentService.confirm_payment_step2(payload=payload)

    if not ret:
        return JSONResponse(content={"msg": "error"}, status_code=HTTPStatus.BAD_REQUEST)

    return ret


@router.post(
    "/{payment_gate}/success/",
    summary="Post event message info",
    description="Post event message info",
)
async def gate_success(payload: PaymentCallbackIn, payment_gate: str):
    ret = await PaymentService.confirm_payment_step1(payload=payload)

    if not ret:
        return JSONResponse(
            content={"msg": "error"}, status_code=HTTPStatus.BAD_REQUEST
        )

    return ret


@router.post(
    "/{payment_gate}/fail/",
    summary="Post event message info",
    description="Post event message info",
)
async def gate(payload: PaymentCallbackIn, payment_gate: str):
    await PaymentService.fail_payment(payload=payload)
    return "OK"
