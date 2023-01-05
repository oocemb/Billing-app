from uuid import UUID
from datetime import date, datetime

from dateutil import relativedelta
from piccolo.columns.combination import WhereRaw

from billing.models import COUPON_TYPE, STATUS
from billing.models import Coupon, UserSubscribe


MINIMAL_PRICE = 10

class CouponService:
    @staticmethod
    async def get_by_title(coupon_title: str) -> Coupon:
        coupon = (
            await Coupon.objects()
            .where((Coupon.title == coupon_title))
            .order_by(Coupon.created_at, ascending=False)
            .first()
        )

        return coupon

    @staticmethod
    async def get_valid_by_title(coupon_title: str) -> Coupon:
        coupon = (
            await Coupon.objects()
            .where(
                (Coupon.title == coupon_title)
                & (Coupon.status == STATUS.ENABLED)
                & (
                    (Coupon.use_max_limit == 0)
                    | (
                        (Coupon.use_max_limit > 0)
                        & (WhereRaw("use_max_limit > use_counter"))
                    )
                )
                & (
                    (Coupon.has_deadline == False)
                    | (
                        (Coupon.has_deadline == True)
                        & (Coupon.deadline >= date.today())
                    )
                )
            )
            .order_by(Coupon.created_at, ascending=False)
            .first()
        )

        return coupon

    @staticmethod
    async def validate(coupon_title) -> bool:
        coupon = await CouponService.get_valid_by_title(coupon_title=coupon_title)

        if coupon:
            return True
        else:
            return False

    @staticmethod
    async def validate_for_subscription(coupon: Coupon, user_id: str) -> bool:
        user_subs = (
            await UserSubscribe.objects()
            .get(UserSubscribe.user == user_id)
            .order_by(UserSubscribe.created_at, ascending=False)
            .first()
        )

        start_date = user_subs.created_at
        now_date = date.today()

        date_delta = relativedelta.relativedelta(start_date, now_date)
        months = date_delta.months + (12 * date_delta.years)

        if months <= coupon.duration_subscribe_months:
            return True
        else:
            return False

    @staticmethod
    async def increment_use_counter(coupon: Coupon):
        if coupon.use_max_limit != 0:
            coupon.use_counter = coupon.use_counter + 1
            await coupon.save()

    @staticmethod
    async def calc_price_first_pay(coupon: Coupon, price: float) -> float:
        if not coupon:
            return price

        is_valid = await CouponService.validate(coupon_title=coupon.title)
        if not is_valid:
            return price

        return await CouponService.calc_price(coupon=coupon, price=price)

    @staticmethod
    async def calc_price_recurrent_pay(
        coupon: Coupon,
        user_id: UUID,
        price: float,
    ) -> float:
        if not coupon:
            return price

        is_valid = await CouponService.validate_for_subscription(
            coupon=coupon, user_id=user_id
        )
        if not is_valid:
            return price

        return await CouponService.calc_price(coupon=coupon, price=price)

    @staticmethod
    async def calc_price(coupon: Coupon, price: float) -> float:
        if coupon.type == COUPON_TYPE.ABSOLUTE:
            if coupon.discount > 0:
                if price > coupon.discount:
                    price = price - coupon.discount
                else:
                    price = MINIMAL_PRICE

        if coupon.type == COUPON_TYPE.PERCENT:
            if 100 > coupon.discount > 0:
                price = price * (1 - coupon.discount / 100)

        return price
