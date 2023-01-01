import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from src.telegram.setup import dp


# You can use state "*" if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def SAny_cancel_handler(message: types.Message, state: FSMContext):
    """ Allow the user to cancel at any point by typing or commanding `cancel` """

    return await cancel_state(message, state)


async def cancel_state(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None: return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply("Ok, bye :(", reply_markup=types.ReplyKeyboardRemove())
