from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import db
from asyncpg import Record, Connection
import re


class EchoItem(BoundFilter):
    key = 'is_echo_item'

    def __init__(self, is_echo_item:bool):
        self.is_echo_item = is_echo_item

    async def check(self, message: types.Message):
        pool: Connection = db
        rec = re.compile(r'\b\w+\s\b\w+')
        item_find = rec.findall(message.text)
        if item_find:
             if await pool.fetchrow('SELECT * FROM test.public.recipes where name = $1 or name_a = $1 or name_b = $1', item_find[0].lower()):
                if self.is_echo_item:
                    return True
                else:
                    return False
        else:
            return False
