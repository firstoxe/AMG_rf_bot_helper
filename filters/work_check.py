from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class WorkCheck(BoundFilter):
    key = 'is_work_contract'

    def __init__(self, is_work_contract: bool):
        self.is_work_contract = is_work_contract

    async def check(self, message: types.Message):
        if message.text.splitlines()[0].find('Работа') != -1 and message.text.splitlines()[4].find('Зависит от уровня профессиональности исполнителя') != -1:
            if self.is_work_contract:
                return True
            else:
                return False
        else:
            return False
