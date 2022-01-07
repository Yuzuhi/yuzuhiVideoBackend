from typing import List, Optional

from sqlalchemy.orm import Session, load_only

from app.models.records import Records
from app.schemas.request import records
from app.service.crud_base import CRUDBase, ModelType
from setting import settings


class CRUDRecords(
    CRUDBase[Records, records.RecordCreate, records.RecordUpdate]
):

    def fetch(self, db: Session, *, user_id: int, video_id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.videoID == video_id, self.model.userID == user_id).first()


crud_records = CRUDRecords(Records)
