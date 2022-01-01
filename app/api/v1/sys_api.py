from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from common import utils
from app.schemas.request.sys_api import ApiCreate, ApiUpdate
from schemas.response import response_code
from service.sys_api import curd_api

router = APIRouter()


@router.post("/add/api", summary="添加API", name="添加API", description="添加API")
async def add_api(
        api_info: ApiCreate,
        db: Session = Depends(utils.get_db),
):
    obj_info = curd_api.create(db, obj_in=api_info)
    return response_code.response_200(data=obj_info)
