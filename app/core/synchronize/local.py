import os
import random
from pathlib import Path
from typing import Set, TypeVar, Union, Generic, Callable, Tuple, Optional

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.custom_exc import LocalEpisodeNameError, LocalVideoTitleError
from app.schemas.request import episodes, videos
from app.service.crud_base import CRUDBase
from app.service.episodes import crud_episodes
from app.service.videos import crud_videos
from setting import settings

CreateSchemaType = TypeVar("CreateSchemaType", bound=videos.VideoCreate)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=videos.VideoUpdate)


class LocalSynchronizer:
    # 自动更新数据库
    AUTO_MODE = "auto"
    # 将本地资源全部同步到数据库上(数据库为空时使用)
    ALL_MODE = "all"
    # 清除数据库上的过时信息
    CLEAR_MODE = 'clear'

    def __init__(self, db: Session, mode: str):
        self.db = db
        self.mode = mode.lower()
        # 初始化添加至数据库的video信息列表
        self.videos_create_list = list()
        # 初始化更新至数据库的video信息列表
        self.videos_update_list = list()
        # 初始化添加至数据库的episode信息列表
        self.episodes_create_list = list()
        # 初始化用于对比本地存储信息与数据库存储信息的set
        self.local_episodes = set()
        self.local_videos = set()

    def synchronize(self):
        # 遍历所有video文件夹
        for video in settings.STATIC_PATH.iterdir():
            self.handle_video_dir(video)

        # 删除本地没有而数据库显示有的本地videos
        if self.mode == self.AUTO_MODE or self.mode == self.CLEAR_MODE:
            # 获取数据库中的所有本地数据的记录
            db_videos = {db_video.id for db_video in crud_videos.get_multi_local(self.db)}
            self._delete_expire_info(crud_videos, db_videos, self.local_videos)

        # 将更新信息上传至数据库
        # try:
        if self.mode == self.CLEAR_MODE:
            return

        if self.videos_create_list:
            crud_videos.multi_create(self.db, obj_list=self.videos_create_list)
        if self.videos_update_list:
            crud_videos.multi_update(self.db, obj_list=self.videos_update_list)
        if self.episodes_create_list:
            crud_episodes.multi_create(self.db, obj_list=self.episodes_create_list)
        # except Exception:
        #     return

    def handle_video_dir(self, video: Path):
        """
        获取一级video文件夹的videoID并处理
        :param video: 视频文件夹的路径
        :return:
        """
        if not video.is_dir():
            return

        if settings.VIDEO_NAME_SEPARATOR in video.name:
            video_info_operate_mode = "update"
            try:
                video_id = self._get_local_episode_id(video)
            except ValueError:
                return
            if self.mode == self.AUTO_MODE or self.mode == self.CLEAR_MODE:
                self.local_videos.add(video_id)
        else:
            if self.mode == self.CLEAR_MODE:
                return
            video_info_operate_mode = "create"
            # 生成一个不重复的video_id,尝试100次
            count = 0
            while count < 100:
                count += 1
                video_id = self.genID(settings.VIDEO_ID_DIGIT)
                res = crud_videos.get(self.db, video_id)
                if not res:
                    # 将文件夹改名
                    title = str(video_id) + settings.VIDEO_NAME_SEPARATOR + video.name
                    os.rename(video, video.parent.joinpath(title))
                    video = Path(title)
                    break
            else:
                return

        self._handle_video_dir(video, video_id, video_info_operate_mode)

    def _handle_video_dir(self, video_path: Path, video_id: int, operate: str):
        """
        处理第一级video文件夹
        :param video_path: 视频文件夹的路径
        :param video_id: 视频文件的id
        :param operate: 对当前video信息的操作方式，如果为create则会添加至数据库，为update则上传至数据库
        :return:
        """
        video_episode = 0
        img = ""
        # 该文件夹下的第一集动画
        first_ep = ""
        for file in video_path.rglob("*"):
            # 封面图
            value = self.handle_file(file, video_path, video_id)
            # 如果value为str,则返回的是img路径，如果value为int，则返回的是episode_id，如果episode_id==-1，则认为此文件为无效文件，跳过。
            if value[0] == 0:
                continue
            elif value[0] == 1:
                img = value[1]
            elif value[0] == 2:
                # 证明当前文件是一个episode
                video_episode += 1
                if not first_ep:
                    first_ep = value[1]

        self._append_video_info(video_id, video_path, img, first_ep, video_episode, operate)

        # 删除过期信息
        if self.mode == self.AUTO_MODE or self.mode == self.CLEAR_MODE:
            # 获取数据库中的该video的episode信息
            db_episodes = {db_episode.id for db_episode in crud_episodes.get_multi_by_videoID(self.db, video_id)}
            self._delete_expire_info(crud_episodes, db_episodes, self.local_episodes)
            # 清空
            self.local_episodes = set()

    def handle_file(self, file: Path, video_path: Path, video_id: int) -> Tuple[int, str]:
        """
        处理二级文件与文件夹
        :param file: 二级文件与文件夹的目录
        :param video_path: 一级文件夹目录
        :param video_id: 一级文件夹ID
        :return: 返回元组，查找到img时元组第1个值返回1，查找到视频文件时元组第1个值返回2，查找到的文件不属于这两种时返回0
        """
        if file.suffix == ".png":
            img = file.relative_to(video_path).as_posix()
            return 1, img
        elif file.suffix == ".mp4":
            if settings.VIDEO_NAME_SEPARATOR in file.name:
                episode_id = self._get_local_episode_id(file)
                if episode_id == -1:
                    return 0, ""
                if self.mode == self.AUTO_MODE or self.mode == self.CLEAR_MODE:
                    self.local_episodes.add(episode_id)
                    return 0, ""
                else:
                    episode_src = self._handle_old_file(episode_id, file, video_id, video_path.name)
                    return 2, episode_src
            else:
                episode_src = self._handle_new_file(file, video_id, video_path.name)
                return 2, episode_src

        return 0, ""

    def _handle_old_file(self,
                         episode_id: int,
                         file: Path,
                         video_id: int,
                         video_name: str,
                         position: str = settings.LOCAL_POSITION) -> str:

        src = settings.STATIC_SERVER + f"{video_name}/{file.parent.name}/{file.name}"
        episode = self._get_local_episode_name(file)

        obj_in = episodes.EpisodeCreate(
            id=episode_id,
            src=src,
            episode=episode,
            type=file.parent.name,
            videoID=video_id,
            position=position,
        )

        self.episodes_create_list.append(obj_in)

        return src

    def _handle_new_file(self,
                         file: Path,
                         video_id: int,
                         video_name: str,
                         position: str = settings.LOCAL_POSITION) -> str:
        episode_id = self.genID(settings.Episode_ID_DIGIT)
        count = 0
        # 最多尝试100次
        while count < 100:
            if crud_episodes.get(self.db, episode_id):
                episode_id = episode_id
                count += 1
            else:
                new_episode_name = str(episode_id) + settings.VIDEO_NAME_SEPARATOR + file.name
                src = settings.STATIC_SERVER + f"{video_name}/{file.parent.name}/{new_episode_name}"

                try:
                    episode = float(file.stem)
                except ValueError:
                    raise LocalEpisodeNameError

                obj_in = episodes.EpisodeCreate(
                    id=episode_id,
                    src=src,
                    episode=episode,
                    type=file.parent.name,
                    videoID=video_id,
                    position=position,
                )
                self.episodes_create_list.append(obj_in)
                # 改名
                os.rename(file, file.parent.joinpath(new_episode_name))
                return src

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

    def _append_video_info(self, video_id: int,
                           video: Path,
                           img: str,
                           first_ep: str,
                           video_episode: int,
                           operate: str):
        """
        :param video_id:
        :param video:
        :param img:
        :param first_ep:
        :param video_episode:
        :param operate: 对当前video信息的操作方式，如果为create则会添加至数据库，为update则上传至数据库
        :return:
        """
        img = settings.STATIC_SERVER + f"{video.name}/{img}"
        title = self._get_local_video_title(Path(video.name))

        if operate == "create":
            obj_in = videos.VideoCreate(
                id=video_id,
                title=title,
                img=img,
                firstEp=first_ep,
                position=settings.LOCAL_POSITION,
                episodes=video_episode
            )

            self.videos_create_list.append(obj_in)
        elif operate == "update":
            obj_in = videos.VideoUpdate(
                id=video_id,
                title=title,
                img=img,
                firstEp=first_ep,
                position=settings.LOCAL_POSITION,
                episodes=video_episode
            )
            self.videos_update_list.append(obj_in)

    @staticmethod
    def _get_local_episode_id(video_path: Path) -> int:
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
        except IndexError:
            raise LocalVideoTitleError

    @staticmethod
    def _get_local_episode_name(video_path: Path) -> float:
        """
        获取本地文件夹或文件的前缀id,如果无法获取则返回-1
        :param video_path:
        :return:
        """
        try:
            return float(video_path.stem.split(settings.VIDEO_NAME_SEPARATOR)[1])
        except ValueError:
            raise LocalEpisodeNameError

    @staticmethod
    def genID(digit: int) -> int:
        return random.randint(0, 10 ** digit - 1)
