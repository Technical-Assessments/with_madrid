import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from src.telegram.setup import bot
from aiogram.dispatcher import FSMContext
from src.utils.framex_utils import FrameXBisector


# States
class Form(StatesGroup):
    name = State()
    pre_game = State()
    in_game = State()
    not_launched = State()


async def has_it_launched(message: Message, state: FSMContext):
    """ Helper function to send new video frames to a Telegram chat room """
    data     : dict           = await state.get_data()
    bisector : FrameXBisector = data["bisector"]
    chat_id  : int            = message.chat.id
    image    : bytes          = bisector.image_frame
    caption  : str            = f"Frame: {bisector.current_frame}"

    # Send Frame
    await bot.send_photo(chat_id=chat_id, photo=image, caption=caption, reply_markup=ReplyKeyboardRemove())

    # Draw Keyboard Options
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Yes", "No")
    markup.add("Cancel")

    text = "Has the rocket launched yet?"
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)


async def cancel_game(message: Message, state: FSMContext):
    """ Allow the user to cancel at any point by typing or commanding `cancel` """

    current_state = await state.get_state()
    data = await state.get_data()
    current_user = data.get("current_user")

    # Cancel state and inform user about it
    logging.info(f"Cancelling state {current_state} for current user: {current_user} ")
    await state.finish()
    await message.reply("Ok, bye :(", reply_markup=ReplyKeyboardRemove())


async def end_game(message: Message, state: FSMContext):
    """ Returns the launch frame and ends the game """

    data         : dict           = await state.get_data()
    current_user : str            = data["current_user"]
    bisector     : FrameXBisector = data["bisector"]

    logging.info(f"Game finished successfuly for current user: {current_user}")

    chat_id = message.chat.id
    text = f"Cheers!! Take-off frame found at step {bisector.step} => {bisector.right_frame}"

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=ReplyKeyboardRemove())
    await state.finish()