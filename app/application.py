from http import HTTPStatus

from core import exceptions
from core.exceptions_handlers import (
    application_error_handler,
    internal_exception_handler,
)
from fastapi import FastAPI

from app.api.routers import command_router, user_router
from app.core.settings import settings


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(title=settings.TITLE, debug=settings.DEBUG, root_path=settings.ROOT_PATH)
    app.include_router(command_router)
    app.include_router(user_router)

    app.add_exception_handler(HTTPStatus.INTERNAL_SERVER_ERROR, internal_exception_handler)
    app.add_exception_handler(exceptions.ApplicationError, application_error_handler)

    return app
