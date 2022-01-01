from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.utils import get_db, genID
from app.core.synchronize.local import LocalSynchronizer

from app.core.video import get_videos_info, get_video_info
from app.models.videos import Videos
from app.schemas.request.episodes import FrontEndEpisodeRetrieve
from app.schemas.request.videos import FrontEndVideoRetrieve
from app.schemas.response import response_code
from app.service.episodes import crud_episodes
from setting import settings
from app.schemas.request import videos, episodes
from app.service.videos import crud_videos

router = APIRouter()


@router.get('/videos/{page}/info')
async def info(page: int, page_size: int = 30, db: Session = Depends(get_db)):
    data = crud_videos.get_multi(db, page=page, page_size=page_size, retrieve_model=FrontEndVideoRetrieve)
    if not data:
        return response_code.response_404()
    return response_code.response_200(data=data)


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


@router.post('/local/synchronize/all')
async def synchronize(db: Session = Depends(get_db)):
    """
    :param db:
    :return:
    """
    ls = LocalSynchronizer(db=db)
    ls.synchronize()
    return response_code.response_200()
