from pathlib import Path
from typing import Union, List

from PIL import Image
from setting import settings


def getImg(path: Path) -> Union[Path, str]:
    for img in path.glob("*"):
        if img.suffix in settings.IMG_FORMAT:
            return img

    return ""


def get_all_episodes(path: Path) -> List[str]:
    """

    :param path: 文件夹路劲
    :return: e.g:[
        "death_note01.mp4",
        "death_note02.mp4"
      ]
    """
    episodes = [file.name for file in path.rglob("*") if file.suffix in settings.VIDEO_FORMAT]
    try:
        episodes.sort(key=lambda x: int(x.split(".")[0]))
    except ValueError:
        pass
    return episodes


def covertImg(title: str,
              img_file: Union[Path, str],
              width: int = settings.PREVIEW_IMG_WIDTH,
              height: int = settings.PREVIEW_IMG_HEIGHT) -> str:
    """将不同大小的图片转换为统一大小,保存在前端项目中的public/preview文件夹下，并返回图片名"""
    if not img_file:
        return ""

    format_name = title + ".png"
    img_link = settings.STATIC_SERVER + f"{title}/{format_name}"

    # 查看静态文件夹下的动画目录中是否有此图片
    format_path = settings.STATIC_PATH.joinpath(title, format_name)
    if format_path.is_file():
        return img_link

    img = Image.open(img_file)
    try:

        # 调整图片大小
        # new_img = img.resize((width, height), Image.BILINEAR)
        # 将图片重命名并保存在其它文件夹
        img.save(str(format_path), format="png")

    except Exception as e:
        return ""

    # 原图片名不规范，弃用此图片名
    # 将原始图片名+上delete后缀来表示此图片已删除
    img_file.rename(str(img_file) + settings.DELETE_SUFFIX)

    return img_link


def get_video_src(title: str, episode: str) -> str:
    video_path = settings.STATIC_PATH.joinpath(title, episode)
    if not video_path.is_file():
        return ""

    return settings.STATIC_SERVER + f"{title}/{episode}"


def get_videos_info() -> list:
    """返回本地存储的剧集信息与预览图"""
    videos = list()

    for video in settings.STATIC_PATH.iterdir():
        # temp dict
        video_dict = dict()
        # temp path
        video_path = settings.STATIC_PATH.joinpath(video)
        # set dict
        video_dict["title"] = video.name
        video_dict["img"] = covertImg(video.name, getImg(video_path))
        video_dict["episodes"] = get_all_episodes(video_path)

        videos.append(video_dict)

    return videos


def get_video_info(title, episode) -> dict:
    data = dict()
    data["src"] = get_video_src(title, episode)
    video_path = settings.STATIC_PATH.joinpath(title)
    data["episodes"] = get_all_episodes(video_path)
    data["img"] = covertImg(title, getImg(video_path))

    return data
