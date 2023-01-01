import dotenv
dotenv.load_dotenv()
import os
from typing import NamedTuple, Text

class Video(NamedTuple):
    name: Text
    width: int
    height: int
    frames: int
    frame_rate: list[int]
    url: Text
    first_frame: Text
    last_frame: Text


class Config(NamedTuple):
    telegram_token = os.getenv("TELEGRAM_TOKEN", "")
    framex_api_url = os.getenv("FRAMEX_API_BASE_URL", "")
    framex_video = os.getenv("FRAMEX_VIDEO", "")