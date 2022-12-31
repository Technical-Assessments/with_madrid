import io
import os
from typing import List, NamedTuple, Text
import requests
from src.framex.utils import bisect


API_BASE = os.getenv("API_BASE", "https://framex-dev.wadrid.net/api/")
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

    def video(self, video: Text) -> Video:
        r = requests.get(f"{API_BASE}video/{video}/")
        return Video(**r.json())

    def video_frame(self, video: Text, frame: int) -> bytes:
        r = requests.get(f"{API_BASE}video/{video}/frame/{frame}/")
        return r.content


class FrameXBisector:
    """
    Helps managing the display of images from the launch
    """

    BASE_URL = API_BASE

    def __init__(self, name):
        self.api = FrameX()
        self.video = self.api.video(name)
        self._index = 0
        self.image = None

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, v):
        """
        When a new index is written, download the new frame
        """

        self._index = v
        self.image = Frame(self.api.video_frame(self.video.name, v))

    @property
    def count(self):
        return self.video.frames




def main():
    """
    Runs a bisection algorithm on the frames of the video, the goal is
    to figure at which exact frame the rocket takes off.

    Images are displayed using pygame, but the interactivity happens in
    the terminal as it is much easier to do.
    """


    def tester(n):
        """
        Displays the current candidate to the user and asks them to
        check if they see wildfire damages.
        """

        bisector.index = n

        confirm_value = confirm(bisector.index)

        return confirm_value

    bisector = FrameXBisector(VIDEO_NAME)

    culprit = bisect(bisector.count, tester)
    bisector.index = culprit

    print(f"Found! Take-off = {bisector.index}")

    exit()