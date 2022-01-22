from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import db
from asyncpg import Record, Connection


class ForwardFromRfBot(BoundFilter):
    key = 'is_from_rf_bot'


    def __init__(self, is_from_rf_bot:bool):
        self.is_from_rf_bot = is_from_rf_bot

    async def check(self, message: types.Message):
        if message.forward_from and message.forward_from.id == 577009581:
            if self.is_from_rf_bot:
                return True
            else:
                return False
        else:
            return False

