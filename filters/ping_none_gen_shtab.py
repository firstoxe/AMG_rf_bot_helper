from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class PingNoneGenShtab(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from and message.forward_from.id == 577009581
                    and (message.text.find('не в ген. штабе]') != -1 or
                    message.text.find('уже совершает действие]') != -1 or
                    message.text.find('выполняют другое действие]') != -1 or
                    message.text.find('выполняет другое действие]') != -1))
