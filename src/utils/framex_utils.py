import logging
from src.framex_api.framex import FrameX
from src.utils.type_helpers import Video
from src.telegram.setup import config

class FrameXBisector:
    """  """

    def __init__(self):
        self.step           : int = 0
        self.video          : Video
        self.total_frames   : int
        self.left_frame     : int
        self.right_frame    : int
        self._current_frame : int
        self.image_frame    : bytes

    async def async_init(self):
        self.video = await FrameX.get_video(config.framex_video)
        self.total_frames = self.video.frames
        self.left_frame = 0
        self.right_frame = self.total_frames - 1
        self._current_frame = self.get_median()
        self.image_frame = await FrameX.get_video_frame(config.framex_video, self.current_frame)

    @property
    def current_frame(self) -> int:
        return self._current_frame

    @current_frame.setter
    def current_frame(self, new_frame: int):
        """ Reactive method to retreive next video frame """
        self.step += 1
        self._current_frame = new_frame

    def launch_frame_found(self) -> bool:
        """ Boolean logic to narrow down the launch video frame """
        return self.left_frame + 1 == self.right_frame

    def get_median(self) -> int:
        """ Return the Median value from two ends """
        return int((self.left_frame + self.right_frame) / 2)

    def bisect(self, tester: bool) -> None:
        """ Performs a binary search """

        mid = self.get_median()

        if tester:
            self.right_frame = mid
        else:
            self.left_frame = mid

        logging.info(f"Step {self.step} => left: {self.left_frame} <-----> right: {self.right_frame}")