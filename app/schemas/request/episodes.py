import time

from pydantic import BaseModel


class EpisodesCreate(BaseModel):
    src: str
    name: str
    type: str
    id: int
    position: str
    videoID: int
    timestamp: float = time.time()


class EpisodesUpdate(BaseModel):
    src: str
    name: str
    type: str
    id: int
    position: str
    videoID: int
    timestamp: float = time.time()


class FrontEndEpisodeRetrieve(BaseModel):
    src: str
    name: str
    type: str
