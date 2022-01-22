from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class GuikdSkladCheck(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from and message.forward_from.id == 577009581
                    and message.text.find('(') != -1 and message.text.find(')') != -1
                    and message.text.find('ур.') != -1 and message.text.find('/a_return_') == -1
                    and message.text.find('Опыт:') == -1 and message.text.find('Баллы:') == -1
                    and message.text.find('/group_') == -1 and message.text.find('Баллы:') == -1
                    and message.text.splitlines()[0] != 'Ресурсы:'and message.text.find('Максимальный уровень тотема') == -1 )
