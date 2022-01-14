from typing import List

from sqlalchemy.orm import Session

from app.common.utils import timeline_rollback, get_db
from app.models.videos import Videos
from app.schemas.request import records
from app.service.records import crud_records


def record_view_history(db: Session, user_id: int, video_id: int, episode_id: int, src: str, timeline: float):
    """
    查询用户是否有看过该video，如果有则更新此条记录，没有则创建
    :param db:
    :param user_id:
    :param video_id:
    :param episode_id:
    :param src:
    :param timeline:
    :return:
    """
    record_obj = crud_records.query(db, video_id=video_id, user_id=user_id)
    # 回溯timeline
    timeline = timeline_rollback(timeline)

    if not record_obj:
        obj_in = records.RecordCreate(
            userID=user_id,
            videoID=video_id,
            episodeID=episode_id,
            src=src,
            timeline=timeline
        )
        crud_records.create(db, obj_in=obj_in)
    else:
        obj_in = records.RecordUpdate(
            episodeID=episode_id,
            src=src,
            timeline=timeline
        )
        crud_records.update(db, record_obj.id, obj_in=obj_in)


def load_user_history(ip: str, videos_info: List[Videos], db: Session = next(get_db())) -> List[Videos]:
    records_obj = crud_records.query_multi(db, ip=ip)

    if not records_obj:
        return videos_info

    records_dict = {record_obj.videoID: record_obj for record_obj in records_obj}

    for video_info in videos_info:
        if records_dict.get(video_info.id, None):
            video_info.timeline = records_dict[video_info.id].timeline
            video_info.firstEp = records_dict[video_info.id].episodeID
        else:
            setattr(video_info, "timeline", 0)

    return videos_info
