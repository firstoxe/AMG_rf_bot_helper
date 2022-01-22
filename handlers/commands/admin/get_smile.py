import asyncio

from aiogram import types
from loader import dp, db
from aiogram.types.chat import ChatType
from aiogram.utils.emoji import demojize
from utils.misc import rate_limit
from data.config import admins
from asyncpg import Connection, Record


@rate_limit(0, 'get_smile')
@dp.message_handler(user_id=admins, chat_type="private", commands='get_smile',)
async def bot_command_rf_actions(message: types.Message):
    await message.answer(demojize(message.text))

