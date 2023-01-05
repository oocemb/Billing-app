from fastapi import APIRouter

from billing.view_models import CouponStatusOut
from billing.service.coupon_service import CouponService

router = APIRouter()


@router.get(
    "/{coupon_title}/status/",
    response_model=CouponStatusOut,
    summary="Get coupon status",
)
async def check_coupon_statue(coupon_title: str) -> CouponStatusOut:
    is_valid = await CouponService.validate(coupon_title=coupon_title)
    return CouponStatusOut(title=coupon_title, is_valid=is_valid)
