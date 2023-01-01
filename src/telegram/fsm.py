import logging
import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from src.utils.telegram_utils import Form, has_it_launched
from src.telegram.setup import dp, bot
from src.telegram.setup import bisector


@dp.message_handler(commands="start")
async def S001_start(message: types.Message):
    """ Be polite and ask the user for his/her name """

    await Form.pre_game.set()
    await message.reply("Hi there! What's your name?")


@dp.message_handler(state=Form.pre_game)
async def S002_game_request(message: types.Message):
    """ Ask the user if he feels playful """

    await message.reply(md.text(f"Hi! Nice to meet you {md.bold(message.text)}"))
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
async def S003_send_first_frame(message: types.Message):
    """ Start the game by sending the first video frame """
    await Form.not_launched.set()
    await has_it_launched(message)


@dp.message_handler(state=Form.not_launched)
async def S004_narrow_frames_down(message: types.Message, state: FSMContext):
    """  """
    tester = True if message.text == "Yes" else False

    if bisector.launch_frame_not_found():
        bisector.bisect(tester=tester)
        logging.info(f"Step {bisector.step} => left: {bisector.left_frame} <-----> right: {bisector.right_frame}")

        await message.reply("I see, so it hasn't launched yet...", reply_markup=types.ReplyKeyboardRemove())
        await has_it_launched(message)

    else:
        text = f"Cheers!! Take-off frame found at step {bisector.step} => {bisector.right_frame}"
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=types.ReplyKeyboardRemove())

        await state.finish()