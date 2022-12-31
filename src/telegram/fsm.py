import logging
import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from src.telegram.cancel import cancel_state
from src.telegram.utils import Form, has_it_launched
from src.telegram.setup import bot, dp




import logging
import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode



@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    # Set state
    await Form.name.set()
    await message.reply("Hi there! What's your name?")


# You can use state "*" if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    return await cancel_state(message, state)


@dp.message_handler(state=Form.name)
async def greet(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data["name"] = message.text

    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Next")
    markup.add("Cancel")

    await message.reply(md.text(
        md.text(f"Hi! Nice to meet you {md.bold(message.text)}")
    ), reply_markup=markup)



@dp.message_handler(state=Form.pre_game)
async def game_request(message: types.Message):
    # Update state and data
    await Form.in_game.set()

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Play the game!")
    markup.add("Cancel")

    await message.reply("Do you want to play DidTheRocketLaunchedYet?", reply_markup=markup)



@dp.message_handler(state=Form.in_game)
async def process_gender(message: types.Message):

    if message.text == "Play the game!":
        # Show first frame

        await Form.not_launched.set()
        await has_it_launched(message)


@dp.message_handler(state=Form.not_launched)
async def process_next_frame(message: types.Message, state: FSMContext):
    print("not launched !")
    await message.reply("I see, so it hasn't launched yet...\n so, has it now?")


@dp.message_handler(state=Form.in_game)
async def end_game(message: types.Message, state: FSMContext):
    await message.reply("NOICE !!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()