from pydantic import BaseModel


class RecordCreate(BaseModel):
    userID: int
    videoID: int
    episodeID: int
    src: str
    timeline: float


class RecordUpdate(BaseModel):
    episodeID: int
    src: str
    timeline: float
