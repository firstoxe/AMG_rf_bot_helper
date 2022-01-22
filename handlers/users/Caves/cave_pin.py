from aiogram import types
from loader import dp, db
from aiogram.types.chat import ChatType
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import demojize,emojize
from data.config import admins
from utils.misc import rate_limit
import logging


@rate_limit(3, 'cave_pin')
@dp.message_handler(commands='cave_pin')
async def bot_command_cave_pin(message: types.Message):
    pool: Connection = db
    usr: Record = await pool.fetch('''SELECT * from test.public.caves 
                                      where league = (select league from test.public.caves where id_leader = $1)
                                      ORDER BY leader_g, room''', message.from_user.id,)
    chat: Record = await pool.fetchrow('''SELECT id_chat from test.public.cave_all_chat 
                                        where league=(select league from test.public.caves where id_leader=$1)''',
                                    message.from_user.id,)
    list_user = []
    if chat:
        if chat[0] == message.chat.id:
            for user in usr:
                list_user.append(f'[{emojize(user["leader_g"])}]{emojize(user["leader_n"])} - {user["room"]}')
            msg = await message.bot.send_message(chat_id=message.chat.id, text='\n\n'.join(list_user))
            await message.bot.pin_chat_message(message_id=msg.message_id, chat_id=msg.chat.id, disable_notification=True)
            arg = msg.message_id, msg.chat.id
            await pool.fetchval('''UPDATE test.public.cave_all_chat SET id_message=$1 where id_chat = $2''', *arg)
    else:
        await message.reply("Данная команда доступна только для лидеров пати находящихся в пещере в соответсвующих чатах")
