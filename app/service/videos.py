from typing import Any, Union, Dict, Sequence, Optional

from sqlalchemy.orm import Session

from app.models.episodes import Episodes
from app.models.videos import Videos
from app.schemas.request import videos

from app.service.crud_base import CRUDBase, ModelType, UpdateSchemaType
from setting import settings


class CRUDVideos(
    CRUDBase[Videos, videos.VideosCreate, videos.VideosUpdate]
):

    def update(self, db: Session, id: int, *, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict(exclude_unset=False)

        update_data = dict()
        for k, v in obj_in.items():
            if obj_in.get(k) != "":
                update_data[k] = v

        db.query(self.model).filter(self.model.id == id).update(update_data, synchronize_session=False)
        db_obj = self.model(**update_data)
        db.commit()
        return db_obj

    def multi_delete(self, db: Session, *, ids: Sequence[int]) -> ModelType:
        # 首先删除episodes表中的数据
        for videoID in ids:
            db.query(Episodes).filter(Episodes.videoID == videoID).filter(
                Episodes.position == settings.LOCAL_POSITION).delete(synchronize_session=False)

        obj = db.query(self.model).filter(self.model.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
        return obj


crud_videos = CRUDVideos(Videos)