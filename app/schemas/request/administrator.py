from pydantic import BaseModel

"""

Request models of administrator

"""


class AdministratorCreate(BaseModel):
    name: str


class AdministratorUpdate(BaseModel):
    id: int
    name: str
