from uuid import UUID
from datetime import date, datetime

from dateutil import relativedelta
from billing.models import SUBSCRIBE_STATUS
from billing.models import UserSubscribe


PAY_FAIL_TRIES = 3


class UserSubscribeService:
    @staticmethod
    async def get_user_subscription(user_id: UUID) -> UserSubscribe:
        subscription = (
            await UserSubscribe.objects()
            .where(UserSubscribe.user == user_id)
            .order_by(UserSubscribe.created_at)
            .first()
        )

        return subscription

    @staticmethod
    async def cancel_user_subscription(user_id: str) -> bool:
        subscription = (
            await UserSubscribe.objects()
            .where(
                (UserSubscribe.user == user_id)
                & (UserSubscribe.subscribe_status == SUBSCRIBE_STATUS.ENABLED)
            )
            .order_by(UserSubscribe.created_at, ascending=False)
            .first()
        )

        if not subscription:
            return False

        subscription.subscribe_status = SUBSCRIBE_STATUS.USER_CANCELED
        await subscription.save()

        return True

    @staticmethod
    async def get_pay_date():
        return datetime.now() - relativedelta.relativedelta(months=1)

    @staticmethod
    async def current_pay_users(batch_size: int):
        pay_date = UserSubscribeService.get_pay_date()

        user_subs = (
            await UserSubscribe.select()
            .where(
                # (UserSubscribe.updated_at == pay_date) and
                (UserSubscribe.subscribe_status == SUBSCRIBE_STATUS.ENABLED)
                and (UserSubscribe.pay_fail_counter <= PAY_FAIL_TRIES)
            )
            .limit(batch_size)
        )

        return user_subs
