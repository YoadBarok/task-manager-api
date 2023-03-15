from pydantic import BaseModel, Field


class User(BaseModel):
    name: str


class RequestUser(BaseModel):
    user: User = Field(...)