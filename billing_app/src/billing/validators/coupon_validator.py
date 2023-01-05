from datetime import date, datetime, relativedelta

from billing.validators.validator import Validator
from piccolo.columns.combination import WhereRaw

from billing.models import Coupon, UserSubscribe
from billing.models import STATUS


class CouponValidator(Validator):
    @staticmethod
    async def validate(**kwargs) -> bool:
        coupon_title = kwargs["coupon_title"]
        ret = await Coupon.count().where(
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
                | ((Coupon.has_deadline == True) & (Coupon.deadline >= date.today()))
            )
        )

        if ret > 0:
            return True
        else:
            return False
