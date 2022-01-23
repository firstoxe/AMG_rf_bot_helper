import typing
from typing import Iterable, Optional, Union
from aiogram.dispatcher.filters.filters import Filter
from aiogram.types import CallbackQuery, ChatType, InlineQuery, Message, ChatMemberUpdated

ChatIDArgumentType = typing.Union[typing.Iterable[typing.Union[int, str]], str, int]


def extract_chat_ids(chat_id: ChatIDArgumentType) -> typing.Set[int]:
    # since "str" is also an "Iterable", we have to check for it first
    if isinstance(chat_id, str):
        return {int(chat_id), }
    if isinstance(chat_id, Iterable):
        return {int(item) for (item) in chat_id}
    # the last possible type is a single "int"
    return {chat_id, }


class CreatorFilter(Filter):
    """
    Checks if user is creator in a chat.
    If is_chat_admin is not set, the filter will check in the current chat (correct only for messages).
    is_creator is required for InlineQuery.
    """

    def __init__(self, is_creator: Optional[Union[ChatIDArgumentType, bool]] = None):
        self._check_current = False
        self._chat_ids = None

        if is_creator is False:
            raise ValueError("is_chat_admin cannot be False")

        if not is_creator:
            self._check_current = True
            return

        if isinstance(is_creator, bool):
            self._check_current = is_creator
        self._chat_ids = extract_chat_ids(is_creator)

    @classmethod
    def validate(cls, full_config: typing.Dict[str, typing.Any]) -> typing.Optional[typing.Dict[str, typing.Any]]:
        result = {}

        if "is_creator" in full_config:
            result["is_creator"] = full_config.pop("is_creator")

        return result

    async def check(self, obj: Union[Message, CallbackQuery, InlineQuery, ChatMemberUpdated]) -> bool:
        user_id = obj.from_user.id

        if self._check_current:
            if isinstance(obj, Message):
                chat = obj.chat
            elif isinstance(obj, CallbackQuery) and obj.message:
                chat = obj.message.chat
            elif isinstance(obj, ChatMemberUpdated):
                chat = obj.chat
            else:
                return False
            if chat.type == ChatType.PRIVATE:  # there is no admin in private chats
                return False
            chat_ids = [chat.id]
        else:
            chat_ids = self._chat_ids

        for chat_id in chat_ids:
            for member in await obj.bot.get_chat_administrators(chat_id):
                if member.status == 'creator' and member.user.id == user_id:
                    return True
        return False
