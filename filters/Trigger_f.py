from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import db
from asyncpg import Record, Connection


class TriggerCheck(BoundFilter):
    key = 'is_trigger'

    def __init__(self, is_trigger: bool):
        self.is_trigger = is_trigger

    async def check(self, message: types.Message):
        pool: Connection = db
        list_triggers: Record = await pool.fetch('''SELECT * FROM test.public.triggers_chat''')
        for item in list_triggers:
            if item["tg_name"] == message.text and item["id_chat"] == message.chat.id:
                if self.is_trigger:
                    return True
        else:
            return False
