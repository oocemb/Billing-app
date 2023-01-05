import uuid
from unittest.mock import MagicMock, patch, AsyncMock

import pytest

# All test coroutines will be treated as marked.
# from main import startup

pytestmark = pytest.mark.asyncio


@pytest.fixture
def payment_sber_data() -> dict:
    """Data for payment by Sber"""

    return {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "coupon": "string",
        "price": 100,
        "is_recurrent": False,
        "payment_provider": "sber",
        "purchased_from_url": "/",
    }


@patch("services.event_service.EventService.send_message")
def test_send_event_message_success(
    send_message_mock: MagicMock, client, payment_sber_data
):
    response = client.post("/api/v1/payment/create/", params=payment_sber_data)
    assert response.status_code == 200
    assert response.json() == {"head": "ok", "body": "all ok"}
    assert send_message_mock.called
