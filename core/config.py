import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "local"
    DEBUG: bool = True

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    SQLALCHEMY_DATABASE_URI: str = f"mysql+aiomysql://root:1234@localhost:3306/food-order"


class DevelopmentConfig(Config):
    ENV: str = "development"
    SQLALCHEMY_DATABASE_URI: str = f"mysql+aiomysql://root:1234@localhost:3306/food-order"


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI: str = f"mysql+aiomysql://root:1234@localhost:3306/food-order"


class ProductionConfig(Config):
    ENV: str = "production"
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = f"mysql+aiomysql://root:1234@localhost:3306/food-order"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config = get_config()
