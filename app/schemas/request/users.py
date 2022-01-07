from pydantic import BaseModel


class UserCreate(BaseModel):
    ip: str


class UserUpdate(BaseModel):
    ip: str
