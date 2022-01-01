import datetime
from sqlalchemy import Column, Integer, VARCHAR, DATETIME, Boolean
from db import Base
from db.session import engine


class Administrator(Base):
    """
    管理员表
    """
    __tablename__ = '(sample)sam_tianchi_mum_baby'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(16), comment='用户名')
    is_super = Column(Boolean, default=False, comment='是否为超级管理员')
    register_date = Column(DATETIME, default=datetime.datetime.now(), comment="注册时间")
    is_del = Column(Boolean, default=False, comment='是否已删除')


Base.metadata.create_all(bind=engine)
