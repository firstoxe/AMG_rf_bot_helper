from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class energyCap(BoundFilter):
    key = 'is_energy_cap'


    def __init__(self, is_energy_cap:bool):
        self.is_energy_cap = is_energy_cap

    async def check(self, message: types.Message):
        if message.text.find('+1 к энергии ') != -1:
            if self.is_energy_cap:
                return True
            else:
                return False
        else:
            return False
