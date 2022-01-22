from datetime import datetime

from aiogram import types
from aiogram.types import ContentType

from aiogram.types.chat import ChatType
from aiogram.utils.emoji import demojize
from asyncpg import Connection, Record

from data.config import admins
from loader import dp, db
from utils.misc import rate_limit
import re


@dp.channel_post_handler(content_types=ContentType.TEXT)
async def bot_command_rf_actions(post: types.Message):
    print(post)