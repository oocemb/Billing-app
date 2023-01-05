from http import HTTPStatus

import pytest

from billing_app.tests.functional.utils.test_errors import TestErrorsStatus

pytestmark = pytest.mark.asyncio


class TestPrice:
    async def test_get_movies(self, make_get_request):
        """Test payment gates list"""
        # Создаем фильмы
        response = await make_get_request("/price/movies/")
        assert response.status == HTTPStatus.OK, TestErrorsStatus.WRONG_STATUS
        # assert type(response.body) == list, TestErrorsStatus.WRONG_RESPONSE
        # sber = list(filter(lambda item: item['short_code'] == 'sber', response.body))

    async def test_get_plans(self, make_get_request):
        """Test payment gates list"""
        # Создаем подписки
        response = await make_get_request("/price/subscriptions/")
        assert response.status == HTTPStatus.OK, TestErrorsStatus.WRONG_STATUS
        # проверка
