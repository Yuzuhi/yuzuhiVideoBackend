from sqlalchemy import Column, Integer, VARCHAR, FLOAT

from app.db import Base
from app.db.session import engine


class Videos(Base):
    """
    videos table
    """
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(64), comment="作品名")
    img = Column(VARCHAR(128), comment="海报地址")
    timestamp = Column(FLOAT, comment="日期时间戳")
    position = Column(VARCHAR(32), comment="作品存放地址（服务器本地还是远程）")
    firstEp = Column(Integer, comment="该动画的第一集的src")
    episodes = Column(Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}.update({"timeline": 0})


Base.metadata.create_all(bind=engine)
