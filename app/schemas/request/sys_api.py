from pydantic import BaseModel

"""

Request models of Api

"""


class ApiCreate(BaseModel):
    path: str
    description: str
    api_group: str
    method: str


class ApiUpdate(BaseModel):
    id: str
