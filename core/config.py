import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "local"
    DEBUG: bool = True

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    DB_URL: str = f"mysql+aiomysql://root:1234@localhost:3306/food-order"
    DB_ECHO: bool = True
    DB_PRE_PING: bool = True


class DevelopmentConfig(Config):
    ENV: str = "development"
    DB_URL: str = f"mysql+aiomysql://root:1234@localhost:3306/food-order"


class LocalConfig(Config):
    DB_URL: str = f"mysql+aiomysql://root:1234@localhost:3306/food-order"


class TestConfig(Config):
    DB_URL: str = f"sqlite+aiosqlite:///:memory:"


class ProductionConfig(Config):
    ENV: str = "production"
    DEBUG: bool = False
    DB_URL: str = f"mysql+aiomysql://root:1234@localhost:3306/food-order"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type[env]


config = get_config()
