from aiogram import types

from keyboards.inline.mob.mob_type import create_cb_mob_type
from loader import dp, db
from aiogram.types.chat import ChatType
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import demojize,emojize
from data.config import admins
from utils.misc import rate_limit
import random
from filters.work_with_user import helper_user



@rate_limit(3, 'mob')
@dp.message_handler(commands='mob')
async def bot_command_mob_e(message: types.Message):
    pool: Connection = db
    user: Record = await pool.fetchrow('''SELECT id,guild,nickname,atk,def,hp,dodge,crit,accuracy,exp_bonus,lvl 
                                          from test.public."user" where id=$1''', message.from_user.id,)
    await message.answer(f'Приветсвую <b>[{user["lvl"]}]</b>{await helper_user(message.from_user.id)}❤{user["hp"]:.{0}f}\n в симуляторе боя с мобами'
                         f'\nВыбери интересущий раздел:', reply_markup=await create_cb_mob_type(message.from_user.id,message.date))
    try:
        await message.delete()
    except:
        pass