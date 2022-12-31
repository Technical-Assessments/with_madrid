from src.setup import dp
from aiogram import types
from src.utils import Form


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.name.set()

    await message.reply("Hi there! What's your name?")