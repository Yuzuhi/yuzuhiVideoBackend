from sqlalchemy.orm import Session

from models.administrator import Administrator
from service.crud_base import CRUDBase
from api.v1 import administrator


class CRUDAdmin(
    CRUDBase[Administrator, administrator.AdministratorCreate, administrator.AdministratorUpdate]
):

    def create(self, db: Session, *, obj_in: administrator.AdministratorCreate) -> Administrator:
        """
        创建角色
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = Administrator(
            name=obj_in.name
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


curd_admin = CRUDAdmin(Administrator)
