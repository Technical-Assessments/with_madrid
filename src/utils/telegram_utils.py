import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from src.telegram.setup import bot
from aiogram.dispatcher import FSMContext

# States
class Form(StatesGroup):
    name = State()
    pre_game = State()
    in_game = State()
    not_launched = State()


async def has_it_launched(message: types.Message, state: FSMContext):

    data = await state.get_data()
    bisector = data.get("bisector")

    # Send Frame
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=bisector.image_frame,
        caption=f"Frame: {bisector.current_frame}",
        reply_markup=types.ReplyKeyboardRemove())

    # Draw Keyboard Options
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Yes", "No")
    markup.add("Cancel")

    await bot.send_message(
        chat_id=message.chat.id,
        text="Has the rocket launched yet?",
        reply_markup=markup)


async def cancel_state(message: types.Message, state: FSMContext):
    """ Allow the user to cancel at any point by typing or commanding `cancel` """

    # current_state = await state.get_state()
    # if current_state is None: return

    data = await state.get_data()
    current_user = data.get("current_user")

    logging.info(f"Cancelling state {current_state} for current user: {current_user} ")
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply("Ok, bye :(", reply_markup=types.ReplyKeyboardRemove())