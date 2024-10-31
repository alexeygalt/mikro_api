from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST"]

    # psql
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    # JWT
    JWT_SECRET_KEY: str
    JWT_ENCODE_ALGORITHM: str

    # google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"

    # yandex
    YANDEX_CLIENT_ID: str
    YANDEX_SECRET_KEY: str
    YANDEX_REDIRECT_URI: str
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    BROKER_URL: str = "localhost:29092"
    EMAIL_TOPIC: str = "email_topic"
    EMAIL_CALLBACK_TOPIC: str = "callback_email_topic"
    # # amqp
    # AMQP_URL: str = 'amqp://guest:guest@localhost:5672//'

    SENTRY_DNS : str

    class Config:
        env_file = ".env"

    @property
    def get_db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_test_db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"

    @property
    def yandex_redirect_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}"


settings = Settings()
