import os

from piccolo.engine.postgres import PostgresEngine

from piccolo.conf.apps import AppRegistry

from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

DB = PostgresEngine(
    config={
        "database": os.getenv("DB_NAME", "billing_database"),
        "user": os.getenv("DB_USER", "app"),
        "password": os.getenv("DB_PASSWORD", "123qwe"),
        "host": os.getenv("HOST", "localhost"),
        "port": os.getenv("PORT", 5434),
    }
)

APP_REGISTRY = AppRegistry(apps=["piccolo_admin.piccolo_app", "billing.piccolo_app"])
