from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str = '127.0.0.1'
    SERVER_PORT: int = 8000
    
    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRES_SEC: int = 3600


settings = Settings(
    _env_file = '.env'
)