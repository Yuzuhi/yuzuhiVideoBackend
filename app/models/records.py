from sqlalchemy import Column, Integer, VARCHAR,FLOAT

from app.db import Base
from app.db.session import engine


class Records(Base):
    """
    records table
    """
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, comment="该记录的用户编号")
    videoID = Column(Integer, comment="用户观看的作品编号")
    episodeID = Column(Integer, comment="用户观看的视频编号")
    src = Column(VARCHAR(128), comment="用户观看的视频src")
    timeline = Column(FLOAT, comment="上次观看的时间轴")


Base.metadata.create_all(bind=engine)
