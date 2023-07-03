from app.api.request_models.request_base import RequestBaseModel


class CommandCreateRequest(RequestBaseModel):
    title: str
    city: str
