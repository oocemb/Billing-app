import os
from pathlib import Path

from pydantic import BaseSettings, Field

4


class TestSettings(BaseSettings):
    service_url: str = f'{os.environ.get("API_HOST", "127.0.0.1")}:{os.environ.get("API_PORT", "5000")}'
    db_name: str = Field(env="DB_NAME", default="billing_database_test")
    db_password: str = Field(env="DB_PASSWORD", default="123qwe")
    db_host: str = Field(env="HOST", default="127.0.0.1")
    db_port: str = Field(env="PORT", default="5434")
    db_user: str = Field(env="DB_USER", default="app")

    api_url: str = "/api/v1"


settings = TestSettings()
