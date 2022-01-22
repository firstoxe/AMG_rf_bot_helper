from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class TotemUpdateFilter(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from and message.forward_from.id == 577009581
                    and ((message.text.find('Тотем') != -1 and message.text.find('Бонус') != -1) or message.text.find('Максимальный уровень тотема') != -1) )
