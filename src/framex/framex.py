import os
from typing import List, NamedTuple, Text
import requests
from src.utils.framex_utils import bisect
from src.utils.http_utils import AioHttpManager


API_BASE = os.getenv("API_BASE", "https://framex-dev.wadrid.net/api/video")
VIDEO_NAME = os.getenv("VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c")



class Video(NamedTuple):
    """
    That's a video from the API
    """

    name: Text
    width: int
    height: int
    frames: int
    frame_rate: List[int]
    url: Text
    first_frame: Text
    last_frame: Text



class FrameX:
    """ Utility class to access the FrameX API """
    def __init__(self) -> None:
        self.session = AioHttpManager()

    def get_video(self, video: Text) -> Video:
        r = requests.get(f"{API_BASE}/{video}/")
        return Video(**r.json())

        # r = await self.session.get(f"{API_BASE}/{video}/")
        # video = Video(** await r.json())
        # return video

    def get_video_frame(self, video: Text, frame: int) -> bytes:
        r = requests.get(f"{API_BASE}/{video}/frame/{frame}/")
        return r.content

        # r = await self.session.get(f"{API_BASE}/{video}/frame/{frame}/")
        # return await self.session.content(r)

class FrameXBisector:
    """ Helps managing the display of images from the launch """

    def __init__(self):
        self.api            : FrameX = FrameX()
        self.video          : Video = self.api.get_video(VIDEO_NAME)
        self.total_frames   : int = self.video.frames
        self.left_frame     : int = 0
        self.right_frame    : int = self.total_frames - 1
        self.current_frame  : int = int((self.left_frame + self.right_frame) / 2)
        self.image          : bytes = self.api.get_video_frame(self.video.name, self.current_frame)


    def launch_frame_not_found(self):
        return self.left_frame + 1 < self.right_frame

    def bisect(self, tester: bool):

        if self.total_frames < 1:
            raise ValueError("Cannot bissect an empty array")

        # while self.left_frame + 1 < self.right_frame:
        mid = int((self.left_frame + self.right_frame) / 2)

        if tester:
            self.right_frame = mid
        else:
            self.left_frame = mid

        # return self.right_frame
