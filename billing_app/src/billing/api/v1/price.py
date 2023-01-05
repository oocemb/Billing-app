import typing as t

from piccolo_api.crud.serializers import create_pydantic_model
from fastapi import APIRouter

from billing.models import MoviePriceTier, SubscriptionPlan

router = APIRouter()

MoviePriceTierModelOut: t.Any = create_pydantic_model(
    table=MoviePriceTier,
    include_default_columns=True,
    model_name="MoviePriceTierModelOut",
)

SubscriptionPlanModelOut: t.Any = create_pydantic_model(
    table=SubscriptionPlan,
    include_default_columns=True,
    model_name="SubscriptionPlanModelOut",
)


@router.get(
    "/movies/",
    response_model=list[MoviePriceTierModelOut],
    summary="List movie prices",
)
async def get_movies():
    return await MoviePriceTier.select().order_by(MoviePriceTier.price)


@router.get(
    "/subscriptions/",
    response_model=list[SubscriptionPlanModelOut],
    summary="List subscriptions prices",
)
async def get_plans():
    return await SubscriptionPlan.select().order_by(SubscriptionPlan.price)
