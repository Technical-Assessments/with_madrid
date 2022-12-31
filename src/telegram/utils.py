from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types


# States
class Form(StatesGroup):
    name = State()
    pre_game = State()
    in_game = State()
    not_launched = State()
    launched = State()


async def has_it_launched(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Yes")
    markup.add("No")
    await message.reply("Has the rocket launched yet?", reply_markup=markup)