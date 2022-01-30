from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class VoteLeader(BoundFilter):
    key = 'vote_leader'

    def __init__(self, vote_leader: bool):
        self.is_energy_cap = vote_leader

    async def check(self, message: types.Message):
        if message.text.count('|') > 9:
            if self.is_energy_cap:
                return True
            else:
                return False
        else:
            return False
