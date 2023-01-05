from uuid import UUID

from pydantic import BaseModel

from billing.models import SubscriptionPlan, MoviePriceTier, STATUS


# Pydantic model for form
class DefaultValuesModel(BaseModel):
    you_email_for_enshure: str = "admin@admin.ru"


# Handler
def default_values_endpoint(request, data):

    try:
        SubscriptionPlan.insert(
            SubscriptionPlan(
                id=UUID("1e1c0173-d419-48a3-b07c-6b56f7d6e41e"),
                title="Basic",
                level=1,
                price=150,
                status=STATUS.ENABLED,
            )
        ).run_sync()

        SubscriptionPlan.insert(
            SubscriptionPlan(
                id=UUID("5e9d9e54-4d2a-4976-bfb6-18b1d2bb7ecf"),
                title="Pro",
                level=2,
                price=250,
                status=STATUS.ENABLED,
            )
        ).run_sync()

        SubscriptionPlan.insert(
            SubscriptionPlan(
                id=UUID("87e0bfd6-e9b9-4f78-b409-4ba4461ed0d3"),
                title="Pro4K",
                level=3,
                price=350,
                status=STATUS.ENABLED,
            )
        ).run_sync()

        MoviePriceTier.insert(MoviePriceTier(title="Free", price=0)).run_sync()
        MoviePriceTier.insert(MoviePriceTier(title="Standart", price=150)).run_sync()
        MoviePriceTier.insert(MoviePriceTier(title="New", price=350)).run_sync()

    except Exception:
        return Exception

    return "ok"
