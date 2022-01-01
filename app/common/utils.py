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


def genID(digit: int) -> int:
    return random.randint(0, 10 ** digit - 1)