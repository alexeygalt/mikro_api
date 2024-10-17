from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'

    class Config:
        env_file = '.env'

    @property
    def get_db_uri(self) -> str:
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def google_redirect_url(self) -> str:
        return f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline'


settings = Settings()
