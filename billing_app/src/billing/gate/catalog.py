from billing.models import PAYMENT_PROVIDER
from billing.gate.payment_robokassa import PaymentRobokassa
from billing.gate.payment_sber import PaymentSber
from billing.gate.payment_yookassa import PaymentYookassa

GATES_PROVIDERS = {
    PAYMENT_PROVIDER.ROBOKASSA: {"provider": PaymentRobokassa, "name": "Robokassa"},
    PAYMENT_PROVIDER.SBER: {"provider": PaymentSber, "name": "Sber Pay"},
    PAYMENT_PROVIDER.YOOKASSA: {"provider": PaymentYookassa, "name": "Yoo Kassa"},
}


def get_payment_provider(payment_method):
    if payment_method not in GATES_PROVIDERS:
        return None
    return GATES_PROVIDERS[payment_method]["provider"]


def get_payment_provider_fabric(payment_method):
    provider_callable = get_payment_provider(payment_method)
    return provider_callable()
