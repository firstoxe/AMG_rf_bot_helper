from aiogram import types
from loader import dp, db
from asyncpg import Connection, Record
from utils.misc import rate_limit
from aiogram.utils.exceptions import BotBlocked, NotEnoughRightsToRestrict
from datetime import datetime, timedelta
import calendar


@rate_limit(1, 'ro')
@dp.message_handler(chat_type='group', is_chat_admin=True, commands='ro', commands_prefix='!/')
async def bot_no_ro(message: types.Message):
    await message.answer('Данный чат не является супергруппой\nВыдача ограничений доступна только в супергруппе\n'
                         'Что бы сделать чат супергруппой, необходимо назначить 5 или более админов')


@rate_limit(1, 'ro')
@dp.message_handler(chat_type='supergroup', is_chat_admin=True, commands='ro', is_reply=True, commands_prefix='!/')
async def bot_ro(message: types.Message):
    status_user = (await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id))["status"]
    if status_user == 'member':
        acc_right = True
        try:
            time_ban = int(message.text.split(' ', maxsplit=2)[1])
        except:
            time_ban = 1
        try:
            prichina = message.text.split(' ', maxsplit=2)[2]
        except:
            prichina = 'причина не указана'
        dt_obj = datetime.now() + timedelta(hours=-3, minutes=time_ban)
        time_tuple = dt_obj.timetuple()
        timestamp_utc = calendar.timegm(time_tuple)
        who_ban = message.reply_to_message.from_user.id
        min_p = ' min'
        pool: Connection = db
        usr: Record = await pool.fetchrow('''SELECT user_dialog from test.public."user" WHERE id= $1''', who_ban, )
        try:
            await message.chat.restrict(message.reply_to_message.from_user.id,
                                        can_send_messages=False,
                                        until_date=timestamp_utc)
            await message.answer(f'Пользователь заблокирован на {time_ban}{min_p}')
        except NotEnoughRightsToRestrict:
            await message.reply(f'Недостаточно прав!')
            acc_right = False
        if acc_right:
            try:
                if usr[0]:
                    await message.bot.send_message(who_ban, (
                        f'Вы получили ограничение на общение в чате - {message.chat.title}\n'
                        f'Срок блокировки - {time_ban}{min_p}\n'
                        f'Причина - {prichina}'))
            except BotBlocked:
                arg = False, who_ban
                await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)
    elif status_user in ['administrator', 'creator']:
        await message.reply('Нельза заблокировать администратора чата')
