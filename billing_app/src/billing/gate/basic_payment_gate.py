from abc import ABC, abstractmethod
from urllib.parse import urlparse


class BasicPaymentGate(ABC):
    def __init__(self):
        self.SAVE_PAYMENT_METHOD = False
        self.CALLBACK_METHOD = "GET"
        self.RECURRENT_SUPPORTED = False

    @staticmethod
    def _parse_response(request: str) -> dict:
        params = {}
        split_query = urlparse(request).query.split("&")
        for item in split_query:
            key, value = item.split("=")
            params[key] = value

        return params

    @abstractmethod
    async def create_new_payment_url(self, *args, **kwargs):
        """Create new URL payment to redirect user to Provider."""
        raise NotImplementedError()

    @abstractmethod
    async def process_recurrent_payment(self, *args, **kwargs):
        """Process new recurrent payment."""
        raise NotImplementedError()

    @abstractmethod
    async def process_callback_data(self, *args, **kwargs):
        """Process provider callback"""
        raise NotImplementedError()

    @abstractmethod
    async def cancel_recurrent_payment(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def refund_payment(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_callback_url(self):
        """Callback URL."""
        raise NotImplementedError()

    @abstractmethod
    def get_success_url(self):
        """Success URL."""
        raise NotImplementedError()

    @abstractmethod
    def get_failed_url(self):
        """Fail URL"""
        raise NotImplementedError()
