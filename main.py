from aiogram.utils import executor
from src.telegram.fsm import dp
from src.telegram.cancel import dp


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)