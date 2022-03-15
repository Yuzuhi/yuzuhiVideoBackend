from pathlib import Path
from typing import Optional, List

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    RELOAD: bool = False
    PORT: int = 8022
    # project document
    TITLE: str = "Yuzuhi Video"
    DESCRIPTION: str = "Yuzuhi Video Backend system"
    # doc url default:/api/docs
    DOCS_URL: str = "/api/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/api/openapi.json"
    # redoc document
    REDOC_URL: Optional[str] = "/api/redoc"
    # token expire time(minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # algorithm of generate token
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = 'aeq)s(*&(&)()WEQasd8**&^9asda_asdasd*&*&^+_sda'
    # root path
    BASE_PATH: str = ""
    # Project
    VIDEO_FORMAT: List[str] = [".mp4", ".mkv", ".rmvb", ".flv"]
    IMG_FORMAT: List[str] = [".png", ".jpeg", ".jpg"]
    PREVIEW_IMG_WIDTH: int = 380
    PREVIEW_IMG_HEIGHT: int = 540
    DELETE_SUFFIX: str = ".delete"
    FIRST_CHAR_OF_FORMAT_VIDEO_NAME: str = "第"
    LAST_CHAR_OF_FORMAT_VIDEO_NAME: str = "話"
    # 视频名的分割符
    VIDEO_NAME_SEPARATOR: str = "$$"
    # 视频id位数
    VIDEO_ID_DIGIT: int = 8
    Episode_ID_DIGIT: int = 10
    # 本地位置
    LOCAL_POSITION = "local"
    # static server
    STATIC_SERVER_HOST: str = "127.0.0.1"
    STATIC_SERVER = f"http://{STATIC_SERVER_HOST}:9000/"
    STATIC_PATH: Path = Path(r"D:\staticServer\Nginx\static")
    # DB
    SQLALCHEMY_DATABASE_URL = "sqlite:///yuzuhiVideo.sqlite"


settings = Settings()
if not settings.DEBUG:
    settings.STATIC_SERVER_HOST = "20.48.90.49"
    settings.STATIC_PATH = Path(r"C:\Users\yuzuhi\Desktop\static")
    settings.STATIC_SERVER = f"http://{settings.STATIC_SERVER_HOST}/"
