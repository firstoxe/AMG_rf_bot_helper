from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AucItemCheck(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from and message.forward_from.id == 577009581 and message.text.find('/a_buy_') !=-1 and message.text.find('ур.') !=-1)
