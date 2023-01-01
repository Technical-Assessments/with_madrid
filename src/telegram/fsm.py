import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from src.utils.framex_utils import FrameXBisector
from src.utils.telegram_utils import Form, has_it_launched, cancel_state
from src.telegram.setup import dp, bot


@dp.message_handler(commands="start")
async def S001_start(message: types.Message, state: FSMContext):
    """ Be polite and ask the user for his/her name """
    user = f"{message.from_user.first_name} {message.from_user.last_name}"
    await state.update_data(current_user=user)

    logging.info(f"Conversation started with {user}")

    await Form.pre_game.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Nice to meet you Bot!")
    markup.add("Cancel")

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello {user} !",
        reply_markup=markup)


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def SAny_cancel_handler(message: types.Message, state: FSMContext):
    """ Allow the user to cancel at any point by typing or commanding `cancel` """

    return await cancel_state(message, state)


@dp.message_handler(state=Form.pre_game)
async def S002_game_request(message: types.Message):
    """ Ask the user if he feels playful """

    await Form.in_game.set()

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Play the game!")
    markup.add("Cancel")

    await bot.send_message(
        chat_id=message.chat.id,
        text="Do you want to play DidTheRocketLaunchedYet?",
        reply_markup=markup)


@dp.message_handler(state=Form.in_game)
async def S003_send_first_frame(message: types.Message, state: FSMContext):
    """ Start the game by sending the first video frame """
    await state.update_data(bisector=FrameXBisector())
    await Form.not_launched.set()
    await has_it_launched(message, state)


@dp.message_handler(state=Form.not_launched)
async def S004_narrow_frames_down(message: types.Message, state: FSMContext):
    """  """

    data = await state.get_data()
    bisector:FrameXBisector = data.get("bisector")
    tester = True if message.text == "Yes" else False

    if bisector.launch_frame_not_found():
        bisector.bisect(tester=tester)
        logging.info(f"Step {bisector.step} => left: {bisector.left_frame} <-----> right: {bisector.right_frame}")

        await state.update_data(bisector=bisector)
        await message.reply(
            "I see...so this is not the launch frame, but we are getting closer!",
            reply_markup=types.ReplyKeyboardRemove())

        await has_it_launched(message, state)

    else:
        await state.finish()

        data = await state.get_data()
        current_user = data.get("current_user")
        # await state.update_data(bisector=FrameXBisector())
        logging.info(f"Game finished successfuly for current user: {current_user} ")

        text = f"Cheers!! Take-off frame found at step {bisector.step} => {bisector.right_frame}"
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=types.ReplyKeyboardRemove())
