from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.utils import get_db
from app.core.record import record_view_history, load_user_history
from app.core.synchronize.local import LocalSynchronizer

from app.models.videos import Videos
from app.schemas.request.episodes import FrontEndEpisodeRetrieve
from app.schemas.request.videos import FrontEndVideoRetrieve
from app.schemas.response import response_code
from app.service.episodes import crud_episodes
from app.service.records import crud_records
from app.service.users import crud_users
from setting import settings
from app.schemas.request import videos, episodes, users, records
from app.service.videos import crud_videos

router = APIRouter()


@router.get('/videos/{page}/info')
async def info(page: int, page_size: int = 30, ip: Optional[str] = None, db: Session = Depends(get_db)):
    videos_info = crud_videos.get_multi(db, page=page, page_size=page_size, retrieve_model=FrontEndVideoRetrieve)
    videos_info = load_user_history(ip, videos_info)

    return response_code.response_200(data=videos_info)


@router.get('/video/{eid}')
async def info(eid: int, db: Session = Depends(get_db)):
    if eid == -1:
        return response_code.response_404()
    data = crud_episodes.get(db, eid)
    return response_code.response_200(data=data)


@router.get('/video/{vid}/all')
async def info(vid: int, db: Session = Depends(get_db)):
    obj_info_list = crud_episodes.get_multi_by_videoID(db, vid, retrieve_model=FrontEndEpisodeRetrieve)
    if not obj_info_list:
        return response_code.response_404()
    return response_code.response_200(data=obj_info_list)


@router.get('/video/{vid}/byClassify')
async def info(vid: int, db: Session = Depends(get_db)):
    obj_info_list = crud_episodes.get_multi_by_videoID(db, vid, retrieve_model=FrontEndEpisodeRetrieve)
    if not obj_info_list:
        return response_code.response_404()
    data = list()
    temp_dict = dict()
    for obj_in in obj_info_list:
        temp_dict.setdefault(obj_in.type, [])
        temp_dict[obj_in.type].append(obj_in)
    for v in temp_dict.values():
        data.append(v)
    return response_code.response_200(data=data)


@router.post('/local/synchronize/{mode}')
async def synchronize(mode: str, db: Session = Depends(get_db)):
    """
    :param mode:
    :param db:
    :return:
    """
    if mode not in LocalSynchronizer.__dict__.values():
        return response_code.response_404()

    ls = LocalSynchronizer(db=db, mode=mode)
    ls.synchronize()
    return response_code.response_200()


@router.post("/view/record")
async def record(ip: str, video_id: int, episode_id: int, src: str, timeline: int, db: Session = Depends(get_db)):
    #
    """
    记录用户最后播放的接口
    :param ip:
    :param video_id:
    :param episode_id:
    :param src:
    :param timeline:
    :param db:
    :return:
    """
    record_view_history(db, ip, video_id, episode_id, src, timeline)
    return response_code.response_200()
