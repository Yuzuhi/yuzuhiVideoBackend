from sqlalchemy.orm import Session

from api.v1 import sys_api
from common import utils
from models.sys_api import SysApi
from service.crud_base import CRUDBase


class CRUDApi(
    CRUDBase[SysApi, sys_api.ApiCreate, sys_api.ApiUpdate]
):

    def create(self, db: Session, *, obj_in: sys_api.ApiCreate) -> SysApi:
        """
        创建角色
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = SysApi(
            path=obj_in.path,
            description=obj_in.description,
            api_group=obj_in.api_group,
            method=obj_in.method
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


curd_api = CRUDApi(SysApi)
