from typing import Union
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.utils import get_db
from app.core.record import record_view_history, load_user_history

from app.schemas.request.episodes import FrontEndEpisodeRetrieve
from app.schemas.request.videos import VideosInfoRetrieve, VidRetrieve
from app.schemas.response import response_code
from app.service.episodes import crud_episodes

from app.service.users import crud_users

from app.service.videos import crud_videos

router = APIRouter()


@router.get('/videos/all')
async def all_vid(db: Session = Depends(get_db)):
    obj_data = crud_videos.get_multi(db, retrieve_model=VidRetrieve)
    data = [item.id for item in obj_data]
    return response_code.response_200(data=data)


@router.get('/videos/{page}/info')
async def info(page: Union[int, str], page_size: Union[int, str] = 30, db: Session = Depends(get_db)):
    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        return response_code.response_4001()

    videos_info = crud_videos.get_multi(db, page=page, page_size=page_size, retrieve_model=VideosInfoRetrieve)
    total_page = crud_videos.total_page(db, pagesize=page_size)
    data = dict()
    data["videos"] = videos_info
    data["totalPage"] = total_page

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


@router.post("/view/record")
async def record(vid: int, eid: int, src: str, timeline: float, request: Request, db: Session = Depends(get_db)):
    #
    """
    ?????????????????????????????????
    :param request:
    :param vid:
    :param eid:
    :param src:
    :param timeline:
    :param db:
    :return:
    """
    ip = request.client.host
    user_obj = crud_users.get_by_ip(db, ip)

    # ?????????????????????????????????????????????????????????????????????
    if user_obj:
        record_view_history(db, user_obj.id, vid, eid, src, timeline)

    return response_code.response_200()
