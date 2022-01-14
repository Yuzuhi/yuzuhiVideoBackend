from typing import Generator
import random

from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    获取sqlalchemy会话对象
    :return:
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def timeline_rollback(timeline: float) -> float:
    new = timeline - 5
    return new if new > 0 else 0
