import os, sys
sys.path.append(os.getcwd())
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.utils.type_helpers import Config
config = Config()

from src.utils.framex_utils import FrameXBisector
bisector = FrameXBisector()

bot = Bot(token=config.telegram_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)