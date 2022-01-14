import os
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.utils import get_db
from app.core.synchronize.local import LocalSynchronizer, LocalAdder
from app.schemas.request import users
from app.schemas.response import response_code
from app.service.users import crud_users
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


@router.get('/local/synchronize/{mode}')
async def synchronize(mode: str, db: Session = Depends(get_db)):
    """
    :param mode:auto,all,clear,add
    :param db:
    :return:
    """
    if mode not in LocalSynchronizer.__dict__.values():
        return response_code.response_404()

    ls = LocalSynchronizer(db=db, mode=mode)
    try:
        ls.synchronize()
    except IntegrityError:
        return response_code.response_4001()
    return response_code.response_200()


@router.get('/local/synchronize/add/{title}')
async def add_video(title: str, db: Session = Depends(get_db)):
    """
    :param title:
    :param db:
    :return:
    """

    ls = LocalAdder(db=db)
    obj_data = ls.add(title)
    if not obj_data:
        return response_code.response_4001()

    return response_code.response_200(data=obj_data)


@router.post("/user/add")
async def add(ip: str, db: Session = Depends(get_db)):
    """添加一个新用户"""
    obj_in = users.UserCreate(ip=ip)
    obj_data = crud_users.create(db, obj_in=obj_in)
    return response_code.response_200(data=obj_data)


@router.post("/user/extend")
async def extend(uid: int, ip: str, db: Session = Depends(get_db)):
    """为一个用户增加一段ip"""
    obj_in = users.UserUpdate(ip=ip)
    db_obj = crud_users.update(db, id=uid, obj_in=obj_in)
    if not db_obj:
        return response_code.response_404()
    return response_code.response_200(data=db_obj)
