from fastapi import FastAPI

from app.api.routers import command_router
from app.core.settings import settings


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(title=settings.TITLE, debug=settings.DEBUG, root_path=settings.ROOT_PATH)
    app.include_router(command_router)

    return app
