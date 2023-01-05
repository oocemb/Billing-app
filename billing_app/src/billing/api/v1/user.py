from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from billing.view_models import (
    UserSubscribeStatusOut,
    UserPurchasedMoviesOut,
    UserPurchaseItemOut,
)
from billing.service.user_subscription_service import UserSubscribeService
from billing.service.user_service import UserService
from billing.core.errors import ErrorStatus

router = APIRouter()


@router.get(
    "/{user_id}/status/",
    response_model=UserSubscribeStatusOut,
    summary="Get user subscription status",
    description="Get user subscription status",
)
async def get_status(user_id: str):
    subscription = await UserSubscribeService.get_user_subscription(user_id)

    if not subscription:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=ErrorStatus.SUBSCRIPTION_NOT_FOUND
        )

    status = UserSubscribeStatusOut(
        user_id=subscription.user,
        status=subscription.subscribe_status,
        charge_date=subscription.created_at,
        last_days=10,
    )

    return status


@router.put(
    "/{user_id}/cancel_subscribe/",
    summary="Post event message info",
    description="Post event message info",
)
async def user_subscribe_cancel(user_id: str) -> str:
    ret = await UserSubscribeService.cancel_user_subscription(user_id)

    if not ret:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=ErrorStatus.SUBSCRIPTION_NOT_FOUND
        )

    return "done"


@router.get(
    "/{user_id}/movies/",
    response_model=list[UserPurchasedMoviesOut],
    summary="Get user movies",
    description="Get user movies",
)
async def get_user_movies(user_id: str):
    movies = await UserService.get_user_movies(user_id)

    if not movies:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=ErrorStatus.MOVIES_NOT_FOUND
        )

    movie_orders = []
    for item in movies:
        tmp = UserPurchasedMoviesOut(
            product_id=item["product"], purchase_date=item["created_at"]
        )
        movie_orders.append(tmp)

    return movie_orders


@router.get(
    "/{user_id}/purchase_history/",
    response_model=list[UserPurchaseItemOut],
    summary="Get user purchase history",
    description="Get user purchase history",
)
async def get_history(user_id: str):
    items = await UserService.get_user_purchase_pretty(user_id)

    if not items:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=ErrorStatus.ITEMS_NOT_FOUND
        )

    return items
