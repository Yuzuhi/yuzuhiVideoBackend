from typing import Optional

from sqlalchemy.orm import Session

from app.models.records import Records
from app.models.users import Users
from app.schemas.request import records
from app.service.crud_base import CRUDBase, ModelType



class CRUDRecords(
    CRUDBase[Records, records.RecordCreate, records.RecordUpdate]
):

    def query(self, db: Session, *, user_id: int, video_id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.videoID == video_id, self.model.userID == user_id).first()

    def query_multi(self, db: Session, *, ip: str, users_model: ModelType = Users):
        return db.query(self.model).join(users_model, self.model.userID == users_model.id).filter(
            users_model.ip.contains(ip)).all()

    def fetch(self, db: Session, *, video_id: int, ip: str, users_model: ModelType = Users) -> Optional[ModelType]:
        return db.query(self.model, users_model).join(self.model, users_model.id == self.model.userID).filter(
            self.model.videoID == video_id, users_model.ip.contains(ip)).first()


crud_records = CRUDRecords(Records)
