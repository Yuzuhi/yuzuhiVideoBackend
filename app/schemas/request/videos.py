import time

from pydantic import BaseModel


class VideoCreate(BaseModel):
    id: int
    title: str
    img: str = ""
    episodes: int
    position: str
    firstEp: int
    timestamp: float = time.time()


class VideoUpdate(BaseModel):
    id: int
    title: str
    img: str
    episodes: int
    position: str
    firstEp: int
    timestamp: float = time.time()


class VideosInfoRetrieve(BaseModel):
    id: int
    title: str
    img: str
    firstEp: int
    episodes: int


class VidRetrieve(BaseModel):
    id: int
