from fastapi import FastAPI

from piccolo_admin.endpoints import create_admin, FormConfig

from piccolo.engine import engine_finder
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from billing.endpoints import BillingEndpoint
from billing.piccolo_app import APP_CONFIG
from billing.api.v1 import price, coupon, payment, gate, user, callback
from billing.form.default_values import DefaultValuesModel, default_values_endpoint
from billing.core.config import logger

app = FastAPI(
    routes=[
        Route("/", BillingEndpoint),
        Mount(
            "/admin/",
            create_admin(
                tables=APP_CONFIG.table_classes,
                site_name="Theatr billing admin",
                # Required when running under HTTPS:
                # allowed_hosts=['my_site.com']
                forms=[
                    FormConfig(
                        name="Create Default",
                        pydantic_model=DefaultValuesModel,
                        endpoint=default_values_endpoint,
                    )
                ],
            ),
        ),
        Mount("/static/", StaticFiles(directory="static")),
    ],
)

app.include_router(payment.router, prefix="/api/v1/payment", tags=["Payment"])
app.include_router(
    callback.router, prefix="/api/v1/callback", tags=["Payment Callback"]
)
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(price.router, prefix="/api/v1/price", tags=["Price"])
app.include_router(coupon.router, prefix="/api/v1/coupon", tags=["Coupon"])
app.include_router(gate.router, prefix="/api/v1/gate", tags=["Payment Gate"])


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except ConnectionRefusedError:
        logger.exception("Unable to connect to the database")


@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except ConnectionRefusedError:
        logger.exception("Unable to close connect to the database")
