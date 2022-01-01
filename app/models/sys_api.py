from sqlalchemy import Column, VARCHAR, Integer
from db import Base
from db.session import engine


class SysApi(Base):
    """
    API表
    """
    __tablename__ = 'tb_api'
    id = Column(Integer, primary_key=True, index=True)
    path = Column(VARCHAR(128), comment="API路径")
    description = Column(VARCHAR(64), comment="API描述")
    api_group = Column(VARCHAR(32), comment="API分组")
    method = Column(VARCHAR(16), comment="请求方法")

    __table_args__ = ({'comment': 'API管理表'})


Base.metadata.create_all(bind=engine)
