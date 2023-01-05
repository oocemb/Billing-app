from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.column_types import Varchar


ID = "2022-11-05T22:05:32:142685"
VERSION = "0.92.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="billing", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Payment",
        tablename="payment",
        column_name="payment_provider",
        db_column_name="payment_provider",
        params={
            "choices": Enum(
                "PAYMENT_PROVIDER",
                {"ROBOKASSA": "robo", "SBER": "sber", "YOOKASSA": "yoka"},
            )
        },
        old_params={
            "choices": Enum(
                "PAYMENT_PROVIDER",
                {
                    "ROBOKASSA": "robo",
                    "YANDEX": "yndx",
                    "SBER": "sber",
                    "BINANCE": "bnnc",
                    "YOOKASSA": "yoka",
                },
            )
        },
        column_class=Varchar,
        old_column_class=Varchar,
    )

    return manager
