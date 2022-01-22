from aiogram import types
from loader import dp,db
from asyncpg import Connection, Record

from utils.misc import rate_limit
from aiogram.utils.exceptions import BotBlocked,BadRequest
from datetime import datetime,timedelta
import calendar


@rate_limit(1, 'unro')
@dp.message_handler(chat_type='group', is_chat_admin=True, commands='unro')
async def bot_no_unro(message: types.Message):
    await message.answer('Данный чат не является супергруппой\nВыдача ограничений доступна только в супергруппе\n'
                         'Что бы сделать чат супергруппой, необходимо назначить 5 или более админов')


@rate_limit(1, 'unro')
@dp.message_handler(chat_type='supergroup', is_chat_admin=True, commands='unro')
async def bot_ro(message: types.Message):
    dt_obj = datetime.now() + timedelta(hours=-3, minutes=0)
    time_tuple = dt_obj.timetuple()
    timestamp_utc = calendar.timegm(time_tuple)
    who_ban = message.reply_to_message.from_user.id
    pool: Connection = db
    usr: Record = await pool.fetchrow('''SELECT user_dialog from test.public."user" WHERE id= $1''', who_ban,)
    await message.chat.restrict(message.reply_to_message.from_user.id, can_send_messages=True, until_date=timestamp_utc)
    await message.answer('Пользователь разблокирован')
    try:
        if usr[0]:
            await message.bot.send_message(who_ban, 'C вас сняты ограничения на общение в чате - ' + message.chat.title)
    except BotBlocked:
        arg = False, who_ban
        await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)

