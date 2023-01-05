from http import HTTPStatus

import pytest

from billing_app.tests.functional.utils.test_errors import TestErrorsStatus

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


@pytest.fixture
def payment_data_not_existing_provider() -> dict:
    """Data for payment by Sber"""

    return {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "coupon": "string",
        "price": 100,
        "is_recurrent": False,
        "payment_provider": "sber",
        "purchased_from_url": "/",
    }


class TestPayment:
    async def test_create_payment_sber(
        self, payment_sber_data, make_post_request, settings
    ):
        """Test sber payment"""
        response = await make_post_request("/payment/create/", params=payment_sber_data)
        assert response.status == HTTPStatus.OK, TestErrorsStatus.WRONG_STATUS
        assert "http" in response.body, TestErrorsStatus.WRONG_RESPONSE
        # pay = Payment.select().where(...).first()

    async def test_create_payment_robo(
        self, payment_sber_data, make_post_request, settings
    ):
        """Test sber payment"""
        response = await make_post_request("/payment/create/", params=payment_sber_data)
        assert response.status == HTTPStatus.OK, TestErrorsStatus.WRONG_STATUS
        assert "url" in response.body, TestErrorsStatus.WRONG_RESPONSE

    async def test_create_payment_missing_provider(
        self, payment_data_not_existing_provider, make_post_request, settings
    ):
        """Test payment with missing provider"""
        response = await make_post_request(
            "/payment/create/", params=payment_data_not_existing_provider
        )
        assert response.status == HTTPStatus.NOT_FOUND, TestErrorsStatus.WRONG_STATUS
