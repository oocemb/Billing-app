import logging
from logging import config as logging_config

from pydantic import BaseSettings, Field

from billing.core.logger import LOGGING

logging_config.dictConfig(LOGGING)
logger = logging.getLogger()


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    # Можно переделать названия переменных просто через PROJECT_NAME: str = "Billing API"
    # В BaseSettings автоматически их берёт из env с таким именем
    project_name: str = Field(env="PROJECT_NAME", default="Billing API")
    HOST_NAME = "https://f994-176-59-44-40.eu.ngrok.io"

    sber_success_url: str = Field(
        env="SBER_SUCCESS_URL", default=f"{HOST_NAME}/api/sber/success"
    )
    sber_failure_url: str = Field(
        env="SBER_FAILURE_URL", default=f"{HOST_NAME}/api/sber/fail"
    )
    sber_callback_url: str = Field(
        env="SBER_CALLBACK_URL", default=f"{HOST_NAME}/api/sber/callback"
    )
    sber_login: str = Field(env="SBER_LOGIN", default="")
    sber_password: str = Field(env="SBER_PASSWORD", default="")
    sber_token: str = Field(env="SBER_TOKEN", default="")

    yoka_secret_key: str = Field(
        env="YOKA_SECRET_KEY",
        default="",
    )
    yoka_shop_id: str = Field(env="YOKA_SHOP_ID", default="")
    yoka_success_url: str = Field(
        env="YOKA_SUCCESS_URL", default=f"{HOST_NAME}/api/yoka/success"
    )
    yoka_failure_url: str = Field(
        env="YOKA_FAILURE_URL", default=f"{HOST_NAME}/api/yoka/fail"
    )
    yoka_callback_url: str = Field(
        env="YOKA_CALLBACK_URL", default=f"{HOST_NAME}/api/yoka/callback"
    )

    robo_login: str = Field(env="ROBO_LOGIN", default="")
    robo_password1: str = Field(env="ROBO_PASS1", default="")
    robo_password2: str = Field(env="ROBO_PASS2", default="")
    robo_test_password1: str = Field(
        env="ROBO_TEST_PASS1", default=""
    )
    robo_test_password2: str = Field(
        env="ROBO_TEST_PASS2", default=""
    )
    robo_success_url: str = Field(
        env="ROBO_SUCCESS_URL", default=f"{HOST_NAME}/api/robo/success"
    )
    robo_failure_url: str = Field(
        env="ROBO_FAILURE_URL", default=f"{HOST_NAME}/api/robo/fail"
    )
    robo_callback_url: str = Field(
        env="ROBO_CALLBACK_URL", default=f"{HOST_NAME}/api/robo/callback"
    )


settings = Settings()
logger.info(settings.dict())
