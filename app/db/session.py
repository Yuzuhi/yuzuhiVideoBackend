from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setting import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False})
Sql_engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
