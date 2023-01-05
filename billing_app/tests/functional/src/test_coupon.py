from http import HTTPStatus

import pytest

from billing_app.tests.functional.utils.test_errors import TestErrorsStatus

pytestmark = pytest.mark.asyncio


class TestCoupon:
    async def test_check_coupon_status(self, make_get_request):
        """Test payment gates list"""

    # new_coupon = Coupon()
    # Сохраняем купон
    # await new_coupon.save()
    response = await make_get_request(f"/coupon/{new_coupon.title}/status")
    assert response.status == HTTPStatus.OK, TestErrorsStatus.WRONG_STATUS
    assert response.body["is_valid"] == False, TestErrorsStatus.WRONG_RESPONSE


async def test_check_missing_coupon_status(self, make_get_request):
    """Test payment gates list"""
    response = await make_get_request("/coupon/missing_coupon/status")
    assert response.status == HTTPStatus.OK, TestErrorsStatus.WRONG_STATUS
    assert response.body["is_valid"] == False, TestErrorsStatus.WRONG_RESPONSE
