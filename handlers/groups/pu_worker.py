from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.misc import rate_limit
from loader import dp, db

from asyncpg import Connection, Record
from aiogram.utils.emoji import emojize


@rate_limit(10, 'make_pu')
@dp.message_handler(commands='make_pu', is_admin=True, is_creator=True)
async def bot_pin_msg(message: types.Message):
    pool: Connection = db

    if not await pool.fetchval('''SELECT * FROM test.public.pu_shtab WHERE id_chat = $1''', message.chat.id,):
        if not await pool.fetchval('''SELECT * FROM test.public.pu_chats WHERE id_chat = $1''', message.from_user.id, ):
            if await pool.execute('''INSERT INTO test.public.pu_shtab(id_chat, name_chat, id_admin) VALUES ($1,$2,$3) RETURNING True''', message.chat.id, message.chat.title, message.from_user.id, ):
                await message.reply('ПУ Чат создан')


@rate_limit(2, 'add_pu_admin')
@dp.message_handler(commands='add_pu_admin', is_reply=True)
async def bot_pin_msg(message: types.Message):
    pool: Connection = db
    if await pool.fetchval('''SELECT * FROM test.public.pu_shtab WHERE id_chat = $1 and id_admin = $2''', (message.chat.id,message.from_user.id)):
        if not await pool.fetchval('''SELECT * FROM test.public.pu_chats WHERE id_chat = $1''', message.from_user.id, ):
            if await pool.execute('''INSERT INTO test.public.pu_shtab(id_chat, name_chat, id_admin) VALUES ($1,$2,$3) RETURNING True''', message.chat.id, message.chat.title, message.from_user.id, ):
                await message.reply('ПУ Чат создан')
