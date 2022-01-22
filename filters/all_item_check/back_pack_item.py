from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class BackPackItemCheck(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from and message.forward_from.id == 577009581
                    and message.text.find('Содержимое рюкзака: ') != -1 )