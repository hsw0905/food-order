from starlette.types import ASGIApp, Scope, Receive, Send

from core.db.sqlalchemy import session


class SqlalchemyMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            await session.remove()
