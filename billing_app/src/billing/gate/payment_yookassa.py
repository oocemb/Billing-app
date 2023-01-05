import asyncio
import uuid

import aiohttp
from aiohttp import BasicAuth

from billing.core.config import settings
from billing.gate.basic_payment_gate import BasicPaymentGate
from billing.models import Payment, PAYMENT_STATUS


class PaymentYookassa(BasicPaymentGate):
    """Payment provider for Yookassa
    Docs: https://yookassa.ru/developers
    """

    def __init__(self):
        super().__init__()
        self.CLIENT_URL = settings.HOST_NAME
        self.REGISTER_URL = "https://api.yookassa.ru/v3/payments"
        self.GET_ORDER_STATUS_URL = "https://api.yookassa.ru/v3/payments/"
        self.REFUND_URL = "https://api.yookassa.ru/v3/refunds"
        self.SAVE_METHOD = True
        self.CURRENCY = "RUB"
        self.api_key = settings.yoka_secret_key
        self.shop_id = str(settings.yoka_shop_id)
        self.CALLBACK_METHOD = "POST"
        self.RECURRENT_SUPPORTED = False

    @staticmethod
    def _get_idempotence_key() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def get_payment_id(body) -> str:
        return body["object"]["id"]

    def _get_params(self, payment, recurrent=False):
        params = {
            "amount": {"value": str(payment.price), "currency": self.CURRENCY},
            "confirmation": {
                "type": "redirect",
                "return_url": self.CLIENT_URL + payment.purchased_from_url,
            },
            "capture": True,
            "save_payment_method": "true",
        }
        if recurrent:
            params["payment_method_id"] = payment.payment_method_id
        return params

    def _get_recurrent_params(self, payment_method_id, price):
        params = {
            "amount": {"value": str(price), "currency": self.CURRENCY},
            "capture": True,
            "payment_method_id": payment_method_id,
            "description": "Заказ description",
        }
        return params

    def _get_refund_params(self, payment_id, price):
        params = {
            "amount": {"value": str(price), "currency": self.CURRENCY},
            "payment_id": payment_id,
        }
        return params

    async def create_new_payment_url(self, payment) -> (str, str):
        params = self._get_params(payment)
        headers = {"Idempotence-Key": self._get_idempotence_key()}
        auth = BasicAuth(self.shop_id, self.api_key)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.REGISTER_URL, json=params, headers=headers, auth=auth
            ) as resp:
                if resp.status == 200:
                    result = await resp.json(content_type=None)
                    return result["confirmation"]["confirmation_url"], str(result["id"])
        # todo: if service not response
        return None, None

    async def process_recurrent_payment(self, payment):
        params = self._get_recurrent_params(
            payment_method_id=payment.parent_payment, price=payment.price
        )
        async with aiohttp.ClientSession() as session:
            headers = {"Idempotence-Key": self._get_idempotence_key()}
            auth = BasicAuth(self.shop_id, self.api_key)
            async with session.post(
                self.REGISTER_URL, json=params, headers=headers, auth=auth
            ) as resp:
                result = await resp.json(content_type=None)
                return result["id"]

    async def process_callback_data(self, content):
        return content

    async def _check_status(self, order_id):
        async with aiohttp.ClientSession() as session:
            url = self.GET_ORDER_STATUS_URL + "/" + order_id
            headers = {"Idempotence-Key": self._get_idempotence_key()}
            auth = BasicAuth(self.shop_id, self.api_key)
            async with session.get(url, headers=headers, auth=auth) as resp:
                if resp.status != 200:
                    return
                result = await resp.json(content_type=None)
                return result

    async def check_success_payment(self, request: str) -> bool:
        order_id = self.get_payment_id(request)
        ret = await self._check_status(order_id)
        payment_status = ret["status"]
        # TODO сделать проверку статусов по документу
        # https://yookassa.ru/developers/payment-acceptance/getting-started/payment-process#payment-statuses
        if payment_status == "succeeded ":
            return True
        else:
            return False

    async def cancel_recurrent_payment(self, *args, **kwargs):
        """Платежи проходят через наши запросы, отменять в провайдере их не нужно"""
        raise NotImplementedError()

    async def refund_payment(self, payment):  # not tested
        """
        https://yookassa.ru/developers/api#refund
        :param payment: Payment
        """
        params = self._get_refund_params(payment.external_order_id, payment.price)
        headers = {"Idempotence-Key": self._get_idempotence_key()}
        auth = BasicAuth(self.shop_id, self.api_key)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.REFUND_URL, json=params, headers=headers, auth=auth
            ) as resp:
                if resp.status == 200:
                    result = await resp.json(content_type=None)
                    return str(result["id"])

    @staticmethod
    def get_success_url():
        return settings.yoka_success_url

    @staticmethod
    def get_callback_url():
        return settings.yoka_callback_url

    @staticmethod
    def get_failed_url():
        return settings.yoka_failure_url


#
#
#
#
#
# ========================== Test function ====================================
#
# async def main():
#     provider = PaymentYookassa()
#     pay_new = Payment(
#         user='asasasas',
#         price=1000,
#         payment_provider='yookassa',
#         payment_type='buy',
#         content='content',
#         status=PAYMENT_STATUS.CREATED,
#         coupon='coupon',
#         is_refund=False,
#         purchased_from_url='http://127.0.0.1:8000',
#     )
#     url = await provider.create_new_payment_url(pay_new)
#     print(url)
#
#
# async def status():
#     provider = PaymentYookassa()
#     order_id = '2af5edfc-000f-5000-a000-112724be3cff'
#     stat = await provider._check_status(order_id)
#     print(stat)
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
