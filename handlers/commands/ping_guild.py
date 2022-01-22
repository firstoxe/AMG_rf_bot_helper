from aiogram import types
from loader import dp
from aiogram.utils.text_decorations import html_decoration
from aiogram.utils.emoji import emojize
from utils.misc import rate_limit
from loader import dp,db
from asyncpg import Connection, Record
from asyncio import sleep

@rate_limit(2, 'ping_guild')
@dp.message_handler(commands=['ping_guild'], is_chat_admin=True, chat_type=['group', 'supergroup'])
async def bot_my_id(message: types.Message):
    pool: Connection = db
    guild: Record = await pool.fetch('''SELECT nickname,id from test.public."user" WHERE guild=(SELECT guild from test.public."user" where id =$1)''', message.from_user.id,)
    cc = 0
    ls_ping = []
    for item in guild:
        ls_ping.append(f'<a href="tg://user?id={item[1]}">{emojize(item[0])}</a>')
        cc += 1
        if cc == 3:
            await message.reply('\n'.join(ls_ping))
            await sleep(0.1)
            ls_ping = []
            cc = 0