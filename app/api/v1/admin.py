import os

from fastapi import APIRouter

from app.schemas.response import response_code
from setting import settings

router = APIRouter()


@router.get('/clear/local/all')
async def local_clear():
    for file in settings.STATIC_PATH.rglob("*"):
        if settings.VIDEO_NAME_SEPARATOR in file.stem:
            new_name = file.stem.split(settings.VIDEO_NAME_SEPARATOR)[1]
            new_name = new_name + file.suffix
            os.rename(file, file.parent.joinpath(new_name))
    return response_code.response_200()
