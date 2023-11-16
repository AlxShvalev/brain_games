from app.api.request_models.request_base import RequestBaseModel


class TeamCreateRequest(RequestBaseModel):
    title: str
    city: str
