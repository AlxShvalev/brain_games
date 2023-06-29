from fastapi import FastAPI

from app.core.settings import settings
from app.api.routers import command_router


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.title,
        debug=settings.debug,
        root_path=settings.root_path
    )
    app.include_router(command_router)

    return app
