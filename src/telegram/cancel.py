import logging
from aiogram import types
from aiogram.dispatcher import FSMContext


async def cancel_state(message: types.Message, state: FSMContext):
    """ Allow the user to cancel at any point by typing or commanding `cancel` """

    current_state = await state.get_state()
    if current_state is None: return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply("Ok, bye :(", reply_markup=types.ReplyKeyboardRemove())
