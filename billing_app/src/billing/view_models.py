from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel
from datetime import datetime, date

from billing.models import PAYMENT_TYPE


class GateOut(BaseModel):
    short_code: str
    name: str


class CouponStatusOut(BaseModel):
    title: str
    is_valid: bool


class UserSubscribeStatusOut(BaseModel):
    user_id: UUID
    status: str
    charge_date: datetime
    last_days: int


class UserPurchasedMoviesOut(BaseModel):
    product_id: UUID
    purchase_date: datetime


class UserPurchaseItemOut(BaseModel):
    product_id: UUID
    price: str
    product_type: str
    purchase_date: datetime
    payment_method: str
    is_refund: bool
    coupon: str = ""
    is_recurrent: bool


class PurchaseIn(BaseModel):
    user_id: UUID
    coupon: str
    price: Decimal
    is_recurrent: bool
    payment_provider: str
    purchased_from_url: str
    payment_type: PAYMENT_TYPE
    content: str


class PaymentCallbackIn(BaseModel):
    provider: str
    url: str
    body: dict = {}


class SuccessCallbackOut(BaseModel):
    payment_type: PAYMENT_TYPE
    content: str
    redirect_url: str = ""
    user_id: str = ""
