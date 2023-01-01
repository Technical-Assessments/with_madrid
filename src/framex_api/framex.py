from src.utils.type_helpers import Video
import requests
from src.telegram.setup import config


class FrameX:
    """ Utility class to access the FrameX API """

    def get_video(self, video: str) -> Video:
        r = requests.get(f"{config.framex_api_url}/{video}/")
        return Video(**r.json())

    def get_video_frame(self, video: str, frame: int) -> bytes:
        r = requests.get(f"{config.framex_api_url}/{video}/frame/{frame}/")
        return r.content
