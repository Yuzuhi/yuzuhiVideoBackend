from sqlalchemy import Column, Integer, VARCHAR
from app.db import Base
from app.db.session import engine


class Users(Base):
    """
    users table
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(128), comment="用户ip，可能由多个ip构成")
    is_delete = Column(Integer, comment="1代表删除，0代表未删除", default=0)


Base.metadata.create_all(bind=engine)
