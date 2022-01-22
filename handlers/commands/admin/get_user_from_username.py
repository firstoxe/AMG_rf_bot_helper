import asyncio
from asyncpg import Record, Connection
from aiogram import types
from loader import dp,db
from aiogram.types.chat import ChatType
from aiogram.utils.emoji import demojize
from utils.misc import rate_limit
from data.config import admins
from aiogram.utils.emoji import emojize
from datetime import datetime,timedelta

@rate_limit(0, 'tesss')
@dp.message_handler(user_id=admins, chat_type="private", commands='tesss')
async def bot_command_tesss(message: types.Message):
    pool: Connection = db
    arg = message.date, message.from_user.id
    usr: Record = await pool.fetchrow('''SELECT * from test.public.caves where id_leader= $1''', 878056191,)
    message.text='Ты направляешься в следующую пещеру'
    if usr["start_move"].timestamp() < message.date.timestamp():
        await pool.fetchval('''UPDATE test.public.caves SET start_move=$1 where id_leader = $2''', *arg)
        await message.answer(f'[{emojize(usr["leader_g"])}]{emojize(usr["leader_n"])} сделал ход, прибытие в след пещеру в {(message.date+timedelta(seconds=30)).time()}')
    else:
        pass