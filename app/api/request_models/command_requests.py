from pydantic import BaseModel


class CommandCreateRequest(BaseModel):
    title: str
    city: str
