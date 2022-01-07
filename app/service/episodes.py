from typing import List, Optional

from sqlalchemy.orm import Session, load_only

from app.models.episodes import Episodes
from app.schemas.request import episodes
from app.service.crud_base import CRUDBase, ModelType
from setting import settings


class CRUDEpisodes(
    CRUDBase[Episodes, episodes.EpisodeCreate, episodes.EpisodeUpdate]
):

    def get_multi_by_videoID(
            self, db: Session, video_id: int, *, page: int = 1, page_size: int = 100,
            retrieve_model: Optional[ModelType] = None
    ) -> List[ModelType]:
        temp_page = (page - 1) * page_size
        if not retrieve_model:
            return db.query(self.model).filter(
                self.model.videoID == video_id, self.model.position == settings.LOCAL_POSITION
            ).order_by(self.model.episode).offset(temp_page).limit(page_size).all()
        else:
            return db.query(self.model).options(load_only(*retrieve_model.__fields__.keys())).filter(
                self.model.videoID == video_id, self.model.position == settings.LOCAL_POSITION
            ).order_by(self.model.episode).offset(temp_page).limit(page_size).all()


crud_episodes = CRUDEpisodes(Episodes)
