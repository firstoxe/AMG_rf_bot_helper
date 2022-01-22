from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.misc import rate_limit
from loader import dp, db

from asyncpg import Connection, Record
from aiogram.utils.emoji import emojize


@rate_limit(2, 'pin')
@dp.message_handler(commands='pin')
async def bot_pin_msg(message: types.Message):
    await message.bot.pin_chat_message(chat_id=message.chat.id,
                                       message_id=message.reply_to_message.message_id,
                                       disable_notification=True)
