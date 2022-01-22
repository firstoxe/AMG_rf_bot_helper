from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import db
from asyncpg import Record, Connection


class AmplifierCheck(BoundFilter):
    key = 'is_amplifier'


    def __init__(self, is_amplifier:bool):
        self.is_amplifier = is_amplifier

    async def check(self, message: types.Message):
        if message.forward_from and message.forward_from.id == 577009581:
            if message.text.splitlines()[0].find('Страница усилителя') != -1:
                if self.is_amplifier:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False