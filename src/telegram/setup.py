import os, sys
sys.path.append(os.getcwd())
import dotenv
dotenv.load_dotenv()
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.framex.framex import FrameXBisector


logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv("TELEGRAM_TOKEN")
FRAMEX_API_BASE_URL = os.getenv("FRAMEX_API_BASE_URL")
FRAMEX_VIDEO = os.getenv("FRAMEX_VIDEO")

bisector = FrameXBisector()
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)