from http import HTTPStatus

import pytest

from billing_app.tests.functional.utils.test_errors import TestErrorsStatus

pytestmark = pytest.mark.asyncio


class TestGate:
    async def test_payment_gates_list(self, make_get_request):
        """Test payment gates list"""
        response = await make_get_request("/gate/")
        assert response.status == HTTPStatus.OK, TestErrorsStatus.WRONG_STATUS
        assert type(response.body) == list, TestErrorsStatus.WRONG_RESPONSE
        sber = list(filter(lambda item: item["short_code"] == "sber", response.body))
        assert len(sber) == 1, "Not sberbank provider in gates list"
