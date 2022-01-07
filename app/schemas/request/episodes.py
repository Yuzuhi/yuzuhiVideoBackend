import time

from pydantic import BaseModel


class EpisodeCreate(BaseModel):
    src: str
    episode: float
    type: str
    id: int
    position: str
    videoID: int
    timestamp: float = time.time()


class EpisodeUpdate(BaseModel):
    src: str
    episode: float
    type: str
    id: int
    position: str
    videoID: int
    timestamp: float = time.time()


class FrontEndEpisodeRetrieve(BaseModel):
    src: str
    episode: float
    type: str
