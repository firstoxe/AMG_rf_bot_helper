from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class CaveMoveShag(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from
                    and message.forward_from.id == 577009581
                    and message.text.find('Ты направляешься в следующую пещеру') != -1)


class CaveMoveShagComplite(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from
                    and message.forward_from.id == 577009581
                    and message.text.find('Ты прибыл в пещеру №') != -1)