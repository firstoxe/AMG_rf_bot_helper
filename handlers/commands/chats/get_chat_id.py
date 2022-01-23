from aiogram import types
from loader import dp
from utils.misc import rate_limit


@rate_limit(3, 'get_chat_id')
@dp.message_handler(commands='get_chat_id')
async def bot_get_chat_id(message: types.Message):
    await message.reply(f'{message.chat.id}')
