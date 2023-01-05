import random

from billing.core.config import logger
from billing.gate.basic_payment_gate import BasicPaymentGate
from billing.models import PAYMENT_STATUS


class PaymentDummy(BasicPaymentGate):
    """Payment provider for test"""

    async def create_new_payment_url(self, payment):
        logger.info(payment)
        """Get URL link for payment"""
        response = {"url": "http://127.0.0.1", "order_id": random.randint(1, 9999999)}
        logger.info("Payment created")
        return response

    async def process_recurrent_payment(self, payment):
        """Create recurent payment"""
        logger.info(payment)
        logger.info("Recurrent payment created")
        return {"status": PAYMENT_STATUS.CREATED}

    async def _check_status(self, order_id):
        logger.info(order_id)
        logger.info("Status is created")
        return True

    async def check_success_payment(self, request: str) -> bool:
        order_id = self.get_payment_id(request)
        ret = await self._check_status(order_id)
        return ret

    def get_callback_url(self):
        return "http://127.0.0.1"

    def get_success_url(self):
        return "http://127.0.0.1"

    def get_failed_url(self):
        return "http://127.0.0.1"

    def process_callback_data(self):
        pass

    def cancel_recurrent_payment(self):
        pass

    def refund_payment(self):
        pass
