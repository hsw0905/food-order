from fastapi import FastAPI

from core.config import config
from core.fastapi.middlewares.sqlalchemy import SqlalchemyMiddleware


def init_middleware(fastapi: FastAPI) -> None:
    fastapi.add_middleware(SqlalchemyMiddleware)


def create_app() -> FastAPI:
    fastapi = FastAPI(
        debug=config.DEBUG,
        app_host=config.APP_HOST,
        app_port=config.APP_PORT,
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc"
    )

    init_middleware(fastapi=fastapi)

    print(f"\n💌💌💌FastAPI Config is '{config.ENV}'")

    return fastapi


app: FastAPI = create_app()
