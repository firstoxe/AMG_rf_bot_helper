from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class RecipeUpdate(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from and message.forward_from.id == 577009581
                    and (message.text.find('Рецепт') != -1
                         and message.text.find('Уровень') != -1
                         and message.text.find('Рецепт антиграва') == -1
                         and message.text.find('Награда!') == -1))

class RecipeUpdateOtherBot(BoundFilter):
    async def check(self, message: types.Message):
        return bool(message.forward_from and message.forward_from.id in [980441353, 1058325728]
                    and message.text.find('/info_item_') == -1
                    and message.text.find('/a_buy') == -1
                    and message.text.find('/a_return') == -1)