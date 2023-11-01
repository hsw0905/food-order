from fastapi import FastAPI

from core.config import config


def create_app() -> FastAPI:
    app_ = FastAPI(
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc"
    )

    print(f"\n💌💌💌FastAPI Config is '{config.ENV}'")

    return app_


app: FastAPI = create_app()
