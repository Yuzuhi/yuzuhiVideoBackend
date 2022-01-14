from typing import List, Optional, Any, TypeVar, Union, Dict

from pydantic.main import BaseModel
from sqlalchemy.orm import Session, load_only

from app.models.episodes import Episodes
from app.models.users import Users
from app.schemas.request import episodes, users
from app.service.crud_base import CRUDBase, ModelType
from setting import settings

UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDUsers(
    CRUDBase[Users, users.UserCreate, users.UserUpdate]
):

    def get_by_ip(self, db: Session, ip: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.ip.contains(ip), self.model.is_delete == 0).first()

    def update(self, db: Session, id: int, *, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        db_obj.ip = db_obj.ip + f",{obj_in.ip}"
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_users = CRUDUsers(Users)
