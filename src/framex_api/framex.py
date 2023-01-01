from src.utils.type_helpers import Video
import aiohttp
from src.telegram.setup import config


class FrameX:
    """ Utility class to access the FrameX API """

    @classmethod
    async def get_video(cls, video: str) -> Video:

        url = f"{config.framex_api_url}/{video}/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                return Video(** await r.json())

    @classmethod
    async def get_video_frame(cls, video: str, frame: int) -> bytes:

        url = f"{config.framex_api_url}/{video}/frame/{frame}/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                return await r.read()