import hashlib
import decimal
from urllib import parse

from billing.gate.basic_payment_gate import BasicPaymentGate
from billing.core.config import settings


class PaymentRobokassa(BasicPaymentGate):
    def __init__(self):
        super().__init__()
        self.PAYMENT_URL = "https://auth.robokassa.ru/Merchant/Index.aspx"
        self.LOGIN = settings.robo_login
        self.PASSWORD1 = settings.robo_password1
        self.PASSWORD2 = settings.robo_password2
        self.TEST_PASS1 = settings.robo_test_password1
        self.TEST_PASS2 = settings.robo_test_password2
        self.TEST = True

    @staticmethod
    def _calculate_signature(*args) -> str:
        """Create signature MD5."""
        return hashlib.md5(":".join(str(arg) for arg in args).encode()).hexdigest()

    def _check_signature_result(
        self,
        order_number: int,  # invoice number
        received_sum: decimal,  # cost of goods, RU
        received_signature: hex,  # SignatureValue
        password: str,  # Merchant password
    ) -> bool:
        signature = self._calculate_signature(received_sum, order_number, password)
        if signature.lower() == received_signature.lower():
            return True
        return False

    def _generate_payment_link(
        self,
        merchant_login: str,  # Merchant login
        merchant_password_1: str,  # Merchant password
        price: decimal,  # Cost of goods, RU
        payment_number: int,  # Invoice number
        description: str = "",  # Description of the purchase
    ) -> str:
        """URL for redirection of the customer to the service."""
        signature = self._calculate_signature(
            merchant_login, price, payment_number, merchant_password_1
        )
        data = {
            "MerchantLogin": merchant_login,
            "OutSum": price,
            "InvId": payment_number,
            "Description": description,
            "SignatureValue": signature,
            "IsTest": "1" if self.TEST else "0",
        }
        return f"{self.PAYMENT_URL}?{parse.urlencode(data)}"

    async def create_new_payment_url(self, payment, *args, **kwargs):
        """Payment amount need convert to '00,00' - format"""
        _price = str(payment.price).replace(".", ",")
        if self.TEST:
            _password = self.TEST_PASS1
        else:
            _password = self.PASSWORD1
        url = self._generate_payment_link(
            merchant_login=self.LOGIN,
            merchant_password_1=_password,
            price=_price,
            payment_number=payment.id,
        )
        return url, str(payment.id)

    async def check_success_payment(self, request: str) -> bool:
        """Verification of operation parameters ("cashier check") in SuccessURL script.
        :param request: HTTP parameters
        """
        if self.TEST:
            merchant_password_1 = self.TEST_PASS1
        else:
            merchant_password_1 = self.PASSWORD1
        param_request = self._parse_response(request)
        cost = param_request["OutSum"]
        payment_number = param_request["InvId"]
        signature = param_request["SignatureValue"]
        is_valid = self._check_signature_result(
            payment_number, cost, signature, merchant_password_1
        )
        return is_valid

    def get_payment_id(self, request: str) -> str:
        param_request = self._parse_response(request)
        return param_request["InvId"]

    async def process_callback_data(self, content: str) -> str:
        """Verification of notification (ResultURL).
        :param content: HTTP parameters.
        """
        if self.TEST:
            merchant_password_2 = self.TEST_PASS2
        else:
            merchant_password_2 = self.PASSWORD2
        param_request = self._parse_response(content)
        cost = param_request["OutSum"]
        number = param_request["InvId"]
        signature = param_request["SignatureValue"]
        if self._check_signature_result(number, cost, signature, merchant_password_2):
            return param_request["InvId"]
        return ""

    async def process_recurrent_payment(self, *args, **kwargs):
        """Только по доп. согласованию с робокассой"""
        pass

    def cancel_recurrent_payment(self):
        """Только по доп. согласованию с робокассой"""
        raise NotImplementedError()

    def refund_payment(self):
        raise NotImplementedError()

    @staticmethod
    def get_failed_url():
        return settings.robo_failure_url

    @staticmethod
    def get_success_url() -> str:
        return settings.robo_success_url

    @staticmethod
    def get_callback_url():
        return settings.robo_callback_url
