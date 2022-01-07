from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends

from app.common.utils import timeline_rollback, get_db
from app.models.videos import Videos
from app.schemas.request import users, records
from app.service.records import crud_records
from app.service.users import crud_users


def record_view_history(db: Session, ip: str, video_id: int, episode_id: int, src: str, timeline: int):
    # 获取用户id
    user_obj = crud_users.get(db, ip)

    if not user_obj:
        # 创建新用户
        obj_in = users.UserCreate(ip=ip)
        user_obj = crud_users.create(db, obj_in=obj_in)

    # 查询用户是否有看过该video，如果有则更新此条记录，没有则创建
    record_obj = crud_records.fetch(db, user_id=user_obj.id, video_id=video_id)
    # 回溯timeline
    timeline = timeline_rollback(timeline)

    if not record_obj:
        obj_in = records.RecordCreate(
            userID=user_obj.id,
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


def load_user_history(ip: str, videos_info: List[Videos], db: Session = Depends(get_db)) -> List[Videos]:
    if not ip:

        for video_info in videos_info:
            video_info.timeline = 0
        return videos_info

    user_obj = crud_users.get(db, ip)

    if not user_obj:
        obj_in = users.UserCreate(ip=ip)
        crud_users.create(db, obj_in=obj_in)

        for video_info in videos_info:
            video_info.timeline = 0
    else:
        # 查询观看进度
        for video_info in videos_info:
            record_obj = crud_records.fetch(db, user_id=user_obj.id, video_id=video_info.id)

            if not record_obj:
                video_info.timeline = 0
            else:
                video_info.firstEp = record_obj.src
                video_info.timeline = record_obj.timeline

    return videos_info
