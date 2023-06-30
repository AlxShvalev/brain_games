import uvicorn

from app.application import create_app
from app.core.settings import settings

app = create_app()

if __name__ == "__main__":
    """Starting application."""
    uvicorn.run(app, host=settings.HOST, port=settings.IP_PORT)
