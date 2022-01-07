from typing import List, Optional, Any

from sqlalchemy.orm import Session, load_only

from app.models.episodes import Episodes
from app.models.users import Users
from app.schemas.request import episodes, users
from app.service.crud_base import CRUDBase, ModelType
from setting import settings


class CRUDUsers(
    CRUDBase[Users, users.UserCreate, users.UserUpdate]
):

    def get(self, db: Session, ip: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.ip.contains(ip), self.model.is_delete == 0).first()


crud_users = CRUDUsers(Users)
