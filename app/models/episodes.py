from sqlalchemy import Column, Integer, VARCHAR, FLOAT

from app.db import Base
from app.db.session import engine


class Episodes(Base):
    """
    episodes table
    """
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True)
    src = Column(VARCHAR(128), comment="视频地址")
    name = Column(VARCHAR(64), comment="视频名，通常为数字")
    type = Column(VARCHAR(16), comment="按剧集性质划分的作品类型（TV，剧场版）")
    position = Column(VARCHAR(32), comment="作品存放地址（服务器本地还是远程）")
    videoID = Column(Integer, comment="该剧集所属的作品的id")
    timestamp = Column(FLOAT, comment="日期时间戳")


Base.metadata.create_all(bind=engine)
