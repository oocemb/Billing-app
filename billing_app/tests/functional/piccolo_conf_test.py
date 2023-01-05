from piccolo_conf import *  # noqa
from tests.functional.settings import settings

DB = PostgresEngine(
    config={
        "database": settings.db_name,
        "user": "app",
        "password": settings.db_password,
        "host": settings.db_host,
        "port": settings.db_port,
    }
)
