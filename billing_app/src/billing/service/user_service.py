from uuid import UUID

from billing.models import Payment, UserSubscribe
from billing.models import PAYMENT_STATUS, PAYMENT_TYPE, SUBSCRIBE_STATUS
from billing.view_models import UserPurchaseItemOut


class UserService:
    @staticmethod
    async def get_user_movies(user_id: UUID) -> UserSubscribe:
        movies = (
            await Payment.select(Payment.content, Payment.created_at)
            .where(
                (Payment.user == user_id)
                & (Payment.status == PAYMENT_STATUS.CONFIRMED)
                & (Payment.payment_type == PAYMENT_TYPE.BUY)
                & (Payment.is_refund == False)
            )
            .order_by(Payment.created_at)
        )

        return movies

    @staticmethod
    async def get_user_purchases(user_id: UUID) -> list[Payment]:
        # TODO Вопрос - какие платежи с каким статусом включать в выдачу
        items = (
            await Payment.select(Payment.all_columns(), Payment.coupon.all_columns())
            .where(
                (Payment.user == user_id)
                & (Payment.status == PAYMENT_STATUS.CONFIRMED_STEP2 or Payment.status == PAYMENT_STATUS.CONFIRMED_STEP1)
            )
            .order_by(Payment.created_at)
        )

        # items = await Payment.select().get(Payment.user == user_id).order_by(Payment.created_at)

        return items

    @staticmethod
    async def get_user_purchase_pretty(user_id: UUID) -> list[UserPurchaseItemOut]:
        items = await UserService.get_user_purchases(user_id)

        if not items:
            return False

        history = []
        for item in items:
            is_recurrent = False
            if item["parent_payment"] != UUID("00000000-0000-0000-0000-000000000000"):
                is_recurrent = True

            # todo: UserPurchaseItemOut rename
            tmp = UserPurchaseItemOut(
                product_id=item["content"],
                price=item["price"],
                product_type=item["payment_type"],
                purchase_date=item["updated_at"],
                payment_method=item["payment_provider"],
                is_refund=item["is_refund"],
                coupon=item["coupon.title"] if item["coupon.title"] else "",
                is_recurrent=is_recurrent,
            )
            history.append(tmp)

        return history
