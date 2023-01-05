from fastapi import APIRouter

from billing.gate.catalog import GATES_PROVIDERS
from billing.view_models import GateOut

router = APIRouter()


@router.get(
    "/",
    response_model=list[GateOut],
    summary="List of available payment gates",
    description="List of available payment gates",
)
async def get_payment_gates():
    return [GateOut(short_code=k, name=v["name"]) for k, v in GATES_PROVIDERS.items()]
