import logging
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from src.utils.framex_utils import FrameXBisector
from src.utils.telegram_utils import Form, has_it_launched, cancel_game, end_game
from src.telegram.setup import dp, bot


@dp.message_handler(commands="start")
async def S001_start(message: Message, state: FSMContext):
    """ Be polite and ask the user for his/her name """

    user = f"{message.from_user.first_name} {message.from_user.last_name}"
    await state.update_data(current_user=user)
    logging.info(f"Conversation started with {user}")

    await Form.pre_game.set()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Nice to meet you Bot!")
    markup.add("Cancel")

    await bot.send_message(chat_id=message.chat.id, text=f"Hello {user} !", reply_markup=markup)


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def SAny_cancel_handler(message: Message, state: FSMContext):
    """ Allow the user to cancel at any point by typing or commanding `cancel` """

    return await cancel_game(message, state)


@dp.message_handler(state=Form.pre_game)
async def S002_game_request(message: Message):
    """ Ask the user if he feels playful """
    await Form.in_game.set()

    chat_id = message.chat.id

    # Configure ReplyKeyboardMarkup
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Play the game!")
    markup.add("Cancel")

    text = "Do you want to play DidTheRocketLaunchedYet?"
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)


@dp.message_handler(state=Form.in_game)
async def S003_send_first_frame(message: Message, state: FSMContext):
    """ Start the game by sending the first video frame """

    # Create instance of bisector to pass it across states
    await state.update_data(bisector=FrameXBisector())

    # Set next state & send first video frame
    await Form.not_launched.set()
    await has_it_launched(message, state)


@dp.message_handler(state=Form.not_launched)
async def S004_narrow_frames_down(message: Message, state: FSMContext):
    """  """

    data = await state.get_data()
    bisector:FrameXBisector = data.get("bisector")
    tester = True if message.text == "Yes" else False

    if bisector.launch_frame_found():
        return await end_game(message, state)

    # Bisect current frames and update bisector state
    bisector.bisect(tester=tester)
    await state.update_data(bisector=bisector)

    # Meaningless commnent to allow keyboard remove
    response = "I see...so this is not the launch frame, but we are getting closer!"
    await message.reply(response, reply_markup=ReplyKeyboardRemove())

    # Process next frame
    return await has_it_launched(message, state)