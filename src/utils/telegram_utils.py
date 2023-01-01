from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from src.telegram.setup import bot
from src.telegram.setup import bisector


# States
class Form(StatesGroup):
    name = State()
    pre_game = State()
    in_game = State()
    not_launched = State()


async def has_it_launched(message: types.Message):

    # Send Frame
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=bisector.image_frame,
        reply_markup=types.ReplyKeyboardRemove())

    # Draw Keyboard Options
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Yes", "No")
    markup.add("Cancel")

    await bot.send_message(
        chat_id=message.chat.id,
        text="Has the rocket launched yet?",
        reply_markup=markup)