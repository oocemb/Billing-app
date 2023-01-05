from enum import Enum

import aiohttp

from billing.core.config import settings
from billing.gate.basic_payment_gate import BasicPaymentGate


class SberStatus(Enum):
    CREATED = 0
    SUCCESS_HOLD = 1
    SUCCESS_FULL_PAID = 2
    CANCEL_AUTH = 3
    REFUND = 4
    INIT_AUTH_BANK = 5
    AUTH_CANCEL = 6


class PaymentSber(BasicPaymentGate):
    """Payment provider for Sber
    Docs: https://securepayments.sberbank.ru/wiki/doku.php/main_page
    """

    def __init__(self):
        super().__init__()
        self.LOGIN = settings.sber_login
        self.PASSWORD = settings.sber_password
        self.REGISTER_URL = "https://3dsec.sberbank.ru/payment/rest/register.do"
        self.PAYMENT_ORDER_BINDING_URL = (
            "https://3dsec.sberbank.ru/payment/rest/paymentOrderBinding.do"
        )
        self.GET_ORDER_STATUS_URL = (
            "https://3dsec.sberbank.ru/payment/rest/getOrderStatusExtended.do"
        )

    def get_payment_id(self, request: str) -> str:
        param_request = self._parse_response(request)
        return param_request["orderId"]

    def _get_params(self, payment, recurrent=False):
        params = {
            "amount": int(payment.price * 100),
            "returnUrl": self.get_callback_url(),
            "failUrl": self.get_failed_url(),
            "userName": self.LOGIN,
            "password": self.PASSWORD,
            "orderNumber": payment.id,
            "clientId": str(payment.user),
        }
        if recurrent:
            params["features"] = "AUTO_PAYMENT"
        return params

    def _get_recurrent_params(self, order_id):
        params = {
            "mdOrder": order_id,
            "bindingId": "bindingId",
            "userName": self.LOGIN,
            "password": self.PASSWORD,
        }
        return params

    def _get_status_params(self, order_id):
        params = {
            "orderId": order_id,
            "userName": self.LOGIN,
            "password": self.PASSWORD,
        }
        return params

    async def create_new_payment_url(self, payment) -> (str, str):
        params = self._get_params(payment)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.REGISTER_URL, params=params) as resp:
                result = await resp.json(content_type=None)
                try:
                    if result["errorCode"]:  # todo: if service not response
                        return result["errorMessage"]
                except KeyError:
                    return result["formUrl"], str(result["orderId"])

    async def process_recurrent_payment(self, payment):
        # params = self._get_params(payment, recurrent=True)
        # order_id = ""
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(self.REGISTER_URL, params=params) as resp:
        #         result = await resp.json(content_type=None)
        #         order_id = result.get("orderId")
        #     if order_id:
        #         recurrent_params = self._get_recurrent_params(order_id)
        #         async with session.get(
        #             self.PAYMENT_ORDER_BINDING_URL, params=recurrent_params
        #         ) as resp:
        #             result = await resp.json(content_type=None)
        #             return result
        pass

    async def _check_status(self, order_id):
        params = self._get_status_params(order_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.GET_ORDER_STATUS_URL, params=params) as resp:
                # {'errorCode':'6','errorMessage':'Заказ не найден','merchantOrderParams':[],'transactionAttributes':[],'attributes':[]}
                result = await resp.json(content_type=None)
                return result

    async def check_success_payment(self, request: str) -> bool:
        order_id = self.get_payment_id(request)
        ret = await self._check_status(order_id)
        payment_status = ret["orderStatus"]
        # TODO сделать проверку статусов по документу
        # https://securepayments.sberbank.ru/wiki/doku.php/integration:api:rest:requests:getorderstatusextended_cart
        if (
            payment_status == SberStatus.SUCCESS_HOLD.value
            or payment_status == SberStatus.SUCCESS_FULL_PAID.value
        ):
            return True
        else:
            return False

    def process_callback_data(self, payment, content):
        """ "Сбербанк сделан на данном этапе через 1 этапную проверку без колбэка"""
        raise NotImplementedError()

    async def cancel_recurrent_payment(self, *args, **kwargs):
        """Платежи проходят через наши запросы, отменять в провайдере их не нужно"""
        raise NotImplementedError()

    def refund_payment(self, payment, amount=None):
        raise NotImplementedError()

    @staticmethod
    def get_callback_url():
        return settings.sber_success_url

    @staticmethod
    def get_failed_url():
        return settings.sber_failure_url

    @staticmethod
    def get_success_url() -> str:
        return settings.sber_success_url
