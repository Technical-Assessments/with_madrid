from src.utils.type_helpers import Video
import requests
# from src.utils.http_utils import AioHttpManager
from src.telegram.setup import config
from aiogram.dispatcher.filters import Text


class FrameX:
    """ Utility class to access the FrameX API """

    # def __init__(self) -> None:
    #     self.session = AioHttpManager()

    def get_video(self, video: Text) -> Video:
        r = requests.get(f"{config.framex_api_url}/{video}/")
        return Video(**r.json())

        # r = await self.session.get(f"{API_BASE}/{video}/")
        # video = Video(** await r.json())
        # return video

    def get_video_frame(self, video: Text, frame: int) -> bytes:
        r = requests.get(f"{config.framex_api_url}/{video}/frame/{frame}/")
        return r.content

        # r = await self.session.get(f"{API_BASE}/{video}/frame/{frame}/")
        # return await self.session.content(r)