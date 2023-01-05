from uuid import UUID

from billing.gate.catalog import get_payment_provider, get_payment_provider_fabric
from billing.models import SubscriptionPlan, Payment, Coupon, UserSubscribe
from billing.models import PAYMENT_STATUS, PAYMENT_TYPE, SUBSCRIBE_STATUS, COUPON_TYPE
from billing.service.coupon_service import CouponService
from billing.service.notification_service import NotificationService
from billing.service.user_subscription_service import UserSubscribeService
from billing.view_models import PurchaseIn, PaymentCallbackIn, SuccessCallbackOut

RECURRENT_BATCH_SIZE = 50


class PaymentService:
    @staticmethod
    async def create_new_payment(payment_in: PurchaseIn) -> str:
        coupon = await CouponService.get_by_title(payment_in.coupon)

        price_with_discount = await CouponService.calc_price_first_pay(
            coupon=coupon, price=payment_in.price
        )

        pay_new = Payment(
            user=payment_in.user_id,
            price=price_with_discount,
            price_original=payment_in.price,
            is_auto_recurrent=False,
            payment_provider=payment_in.payment_provider,
            payment_type=payment_in.payment_type,
            content=payment_in.content,
            status=PAYMENT_STATUS.CREATED,
            coupon=coupon,
            is_refund=False,
            purchased_from_url=payment_in.purchased_from_url,
        )
        await pay_new.save()

        if payment_in.payment_type == PAYMENT_TYPE.SUBSCRIBE:
            # todo: get or create
            # todo: if payment.is_recurent UBSCRIBE_STATUS.user otmenil,
            user_subs = UserSubscribe(
                user=payment_in.user_id,
                subscribe_plan=payment_in.content,  # noqa
                coupon=coupon,
                first_payment=pay_new,  # noqa
                subscribe_status=SUBSCRIBE_STATUS.NOT_STARTED,
                pay_fail_counter=0,
            )
            await user_subs.save()

        provider_callable = get_payment_provider(payment_in.payment_provider)
        provider = provider_callable()

        try:
            pay_redirect_url, external_order_id = await provider.create_new_payment_url(
                pay_new
            )
            if external_order_id:
                pay_new.external_order_id = external_order_id
            else:
                pay_new.external_order_id = str(pay_new.id)  # noqa

        except ValueError:
            pay_redirect_url = None
            pay_new.status = PAYMENT_STATUS.ERROR

        finally:
            await pay_new.save()

        return pay_redirect_url

    @staticmethod
    async def confirm_payment_step1(payload: PaymentCallbackIn):
        provider_callable = get_payment_provider(payload.provider)
        provider = provider_callable()
        payment_external = provider.get_payment_id(request=payload.url)
        payment = (
            await Payment.objects()
            .where(Payment.external_order_id == payment_external)
            .first()
        )  # noqa

        is_new_payment = True
        if payment.status == PAYMENT_STATUS.CONFIRMED_STEP2:
            is_new_payment = False

        msg = None

        # Обновление платежа
        success_checked = await provider.check_success_payment(request=payload.url)
        if success_checked:
            payment.status = PAYMENT_STATUS.CONFIRMED_STEP1

            msg = SuccessCallbackOut(
                payment_type=payment.payment_type,
                content=str(payment.content),
                redirect_url=payment.purchased_from_url,
            )
        else:
            payment.status = PAYMENT_STATUS.ERROR

        if is_new_payment:
            await payment.save()

            # Обновление подписки
            if payment.payment_type == PAYMENT_TYPE.SUBSCRIBE and success_checked:
                user_subs = (
                    await UserSubscribe()
                    .objects()
                    .where(UserSubscribe.first_payment == int(payment.id))  # noqa
                    .first()
                )

                user_subs.subscribe_status = SUBSCRIBE_STATUS.ENABLED
                await user_subs.save()

            # обновление купона
            coupon_id = payment.coupon
            if coupon_id:
                coupon = await Coupon.objects().where(Coupon.id == coupon_id).first()
                await CouponService.increment_use_counter(coupon=coupon)

        return msg

    @staticmethod
    async def confirm_payment_step2(payload: PaymentCallbackIn):
        provider_callable = get_payment_provider(payload.provider)
        provider = provider_callable()
        if provider.CALLBACK_METHOD == "POST":
            payment_external = provider.get_payment_id(payload.body)
        else:  # 'get'
            payment_external = provider.get_payment_id(payload.url)
        payment = (
            await Payment.objects()
            .where(Payment.external_order_id == payment_external)
            .first()
        )  # noqa

        if provider.CALLBACK_METHOD == "POST":
            success_checked_data = await provider.process_callback_data(payload.body)
        else:  # 'get'
            success_checked_data = await provider.process_callback_data(payload.url)
        if success_checked_data:
            payment.status = PAYMENT_STATUS.CONFIRMED_STEP2
            if provider.SAVE_PAYMENT_METHOD:
                payment.parent_payment = success_checked_data["object"][
                    "payment_method"
                ]["id"]

        #
        # if provider.check_amount_payment(payload):
        #     payment.status = PAYMENT_STATUS.ERROR
        #     return

        msg = SuccessCallbackOut(
            payment_type=payment.payment_type,
            content=str(payment.content),
            user_id=str(payment.user),
        )

        await payment.save()

        # Если это первый платеж (не рекуррентный) и подписка, то делаем подписку и тратим купон
        if not payment.is_auto_recurrent:
            # Обновление подписки
            if payment.payment_type == PAYMENT_TYPE.SUBSCRIBE and success_checked_data:
                user_subs = (
                    await UserSubscribe()
                    .objects()
                    .where(UserSubscribe.first_payment == int(payment.id))  # noqa
                    .first()
                )

                user_subs.subscribe_status = SUBSCRIBE_STATUS.ENABLED
                await user_subs.save()

            # обновление купона
            coupon_id = payment.coupon
            if coupon_id:
                coupon = await Coupon.objects().where(Coupon.id == coupon_id).first()
                await CouponService.increment_use_counter(coupon=coupon)
        # Отправляем уведомление об успешной оплате пользователю
        await NotificationService.send_success_notification()
        return msg

    @staticmethod
    async def fail_payment(payload: PaymentCallbackIn):
        provider_callable = get_payment_provider(payload.provider)
        provider = provider_callable()
        payment_number = provider.get_payment_id()
        payment = (
            await Payment.objects()
            .where(Payment.external_order_id == payment_number)
            .first()
        )  # noqa

        payment.status = PAYMENT_STATUS.REJECTED
        # Отправляем уведомление об неудачной оплате пользователю
        await NotificationService.send_fail_notification()
        await payment.save()

    @staticmethod
    async def process_recurrent_payment(first_payment_id: int):
        first_payment = (
            await Payment.objects().where(Payment.id == first_payment_id).first()
        )
        provider = get_payment_provider_fabric(first_payment.payment_provider)
        if not provider.RECURRENT_SUPPORTED:
            return  # Провайдер не поддерживает рекуррентные платежи, добавить в логи ошибку
        coupon = await Coupon.objects().where(Coupon.id == first_payment.coupon).first()

        price_with_discount = await CouponService.calc_price_recurrent_pay(
            coupon=coupon,
            user_id=first_payment.user,
            price=first_payment.price_original,
        )
        pay_new = Payment(
            user=first_payment.user,
            price=price_with_discount,
            parent_payment=first_payment.external_order_id,
            is_auto_recurrent=True,
            price_original=first_payment.price_original,
            payment_provider=first_payment.payment_provider,
            payment_type=first_payment.payment_type,
            content=first_payment.content,
            status=PAYMENT_STATUS.CREATED,
            coupon=coupon,
            is_refund=False,
        )

        try:
            result = await provider.process_recurrent_payment(pay_new)
            pay_new.external_order_id = result
        except ValueError:
            pay_new.status = PAYMENT_STATUS.ERROR
        finally:
            await pay_new.save()

    @staticmethod
    async def recurrent_batch():
        user_subs = await UserSubscribeService.current_pay_users(
            batch_size=RECURRENT_BATCH_SIZE
        )
        for user_sub in user_subs:
            first_payment_id = user_sub["first_payment"]
            await PaymentService.process_recurrent_payment(
                first_payment_id=first_payment_id
            )
