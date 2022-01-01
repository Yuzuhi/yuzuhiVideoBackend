import os
from pathlib import Path
from typing import Set

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.utils import genID
from app.schemas.request import episodes, videos
from app.service.crud_base import CRUDBase
from app.service.episodes import crud_episodes
from app.service.videos import crud_videos
from setting import settings


class LocalSynchronizer:

    def __init__(self, db: Session):
        self.db = db

    def _update_episodes_info_to_db(self,
                                    video_path: Path,
                                    video_id: int,
                                    video_name: str,
                                    check_expire: bool) -> tuple:
        """
        上传video文件夹内的episode信息，并返回该video的封面图src与剧集数
        :param video_path:
        :param video_id:
        :param check_expire:
        :return:
        """
        video_episode = 0
        img = ""
        local_episodes = set()
        db_episodes = set()
        # 该文件夹下的第一集动画
        first_ep = -1

        # 获取当前video的所有剧集数据
        if check_expire:
            db_episodes = {db_episode.id for db_episode in crud_episodes.get_multi_by_videoID(self.db, video_id)}
        for file in video_path.rglob("*"):
            # 封面图
            if file.suffix == ".png":
                # 更新videos图源
                img = file.relative_to(video_path).as_posix()
            elif file.suffix == ".mp4":
                video_episode += 1
                # 检测文件名中是否有分割符，如果没有的话添加分割符并上传至数据库
                if settings.VIDEO_NAME_SEPARATOR in file.name:
                    if check_expire:
                        file_id = self._get_local_file_id(file)
                        if file_id != -1:
                            local_episodes.add(file_id)
                    continue
                # 视频id为10位数
                episode_id = genID(settings.Episode_ID_DIGIT)
                new_episode_name = str(episode_id) + settings.VIDEO_NAME_SEPARATOR + file.name

                src = settings.STATIC_SERVER + f"{video_name}/{file.parent.name}/{new_episode_name}"

                if first_ep == -1:
                    first_ep = episode_id

                while True:
                    try:
                        obj_in = episodes.EpisodesCreate(
                            id=episode_id,
                            src=src,
                            name=file.stem,
                            type=file.parent.name,
                            videoID=video_id,
                            position=settings.LOCAL_POSITION,
                        )
                        crud_episodes.create(self.db, obj_in=obj_in)
                        break
                    except IntegrityError:
                        episode_id = genID(settings.Episode_ID_DIGIT)
                # 改名
                os.rename(file, file.parent.joinpath(new_episode_name))

        if check_expire:
            self._delete_expire_info(crud_episodes, db_episodes, local_episodes)

        return first_ep, img, video_episode

    @staticmethod
    def _get_local_file_id(video_path: Path) -> int:
        """
        获取本地文件夹或文件的前缀id,如果无法获取则返回-1
        :param video_path:
        :return:
        """
        try:
            return int(video_path.name.split(settings.VIDEO_NAME_SEPARATOR)[0])
        except ValueError:
            return -1

    @staticmethod
    def _get_local_video_title(video_path: Path) -> str:
        """
        获取本地文件夹或文件的前缀id,如果无法获取则返回-1
        :param video_path:
        :return:
        """
        try:
            return video_path.name.split(settings.VIDEO_NAME_SEPARATOR)[1]
        except ValueError:
            return ""

    def _delete_expire_info(self, service: CRUDBase, db_info: Set[int], local_info: Set[int]):
        """
        删除数据库中的过期数据
        :param db_info:
        :param local_info:
        :return:
        """
        db_info.difference_update(local_info)
        service.multi_delete(self.db, ids=list(db_info))

    def synchronize(self):
        # 获取数据库中的所有本地数据的记录
        db_videos = {db_video.id for db_video in crud_videos.get_multi_by_position(self.db)}

        # 初始化保存本地videoID的集合
        local_videos = set()
        # 遍历所有本地资源
        for video in settings.STATIC_PATH.iterdir():
            if not video.is_dir():
                continue
            if settings.VIDEO_NAME_SEPARATOR in video.name:
                # 已经被录入数据库的文件夹
                try:
                    video_id = self._get_local_file_id(video)
                except ValueError:
                    continue

                first_ep, img, video_episode = self._update_episodes_info_to_db(video,
                                                                                video_id,
                                                                                video.name,
                                                                                check_expire=True)
                # 找到图片
                if img:
                    img = settings.STATIC_SERVER + f"{video.name}/{img}"

                title = self._get_local_video_title(video)

                if not title:
                    title = video.name

                obj_in = videos.VideosUpdate(
                    id=video_id,
                    title=title,
                    img=img,
                    firstEp=first_ep,
                    position=settings.LOCAL_POSITION,
                    episodes=video_episode)

                crud_videos.update(self.db, video_id, obj_in=obj_in)

                local_videos.add(video_id)
            else:
                # 仍未被录入数据库的文件夹
                video_id = genID(settings.VIDEO_ID_DIGIT)
                # 生成一个不重复的video_id
                while crud_videos.get(self.db, video_id):
                    video_id = genID(settings.VIDEO_ID_DIGIT)

                new_video_name = str(video_id) + settings.VIDEO_NAME_SEPARATOR + video.name

                first_ep, img, video_episode = self._update_episodes_info_to_db(video,
                                                                                video_id,
                                                                                new_video_name,
                                                                                check_expire=False)

                title = str(video_id) + settings.VIDEO_NAME_SEPARATOR + video.name
                img = settings.STATIC_SERVER + f"{title}/{img}"

                obj_in = videos.VideosCreate(
                    id=video_id,
                    title=video.name,
                    img=img,
                    firstEp=first_ep,
                    position=settings.LOCAL_POSITION,
                    episodes=video_episode)

                crud_videos.create(self.db, obj_in=obj_in)
                # 将文件夹改名
                os.rename(video, video.parent.joinpath(title))

        # 验证video数据库中是否有已经被删去的本地数据
        self._delete_expire_info(crud_videos, db_videos, local_videos)
