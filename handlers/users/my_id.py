from aiogram import types


from loader import dp
from utils.misc import rate_limit


@rate_limit(2, 'my_id')
@dp.message_handler(commands=['my_id'])
async def bot_my_id(message: types.Message):
    await message.reply(f'{message.from_user.id}')