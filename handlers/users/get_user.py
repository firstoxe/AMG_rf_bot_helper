from aiogram import types
from loader import dp, db
from aiogram.types.chat import ChatType
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import demojize, emojize
from data.config import admins
from utils.misc import rate_limit
import logging

race_convert = {1: ':woman_astronaut:', 2: ':woman_elf:', 3: ':robot:'}
from filters.guild_check import check_g


@rate_limit(3, 'get_user')
@dp.message_handler(commands='get_user')
async def bot_command_get_user(message: types.Message):
    pool: Connection = db
    try:
        who: Record = await pool.fetchrow('''SELECT * from test.public."user" where id=$1''', message.from_user.id, )
        logging.info(f"[{emojize(who['guild'])}]{emojize(who['nickname'])}({message.from_user.id}) кого то ищет")
        if len(message.text.split(' ')) > 1:
            f_id = 0
            try:
                f_id = int(message.text.split(' ', maxsplit=1)[1])
                user: Record = await pool.fetchrow('''SELECT * from test.public."user" where id=$1''', f_id, )
            except:
                nick = demojize(message.text.split(' ', maxsplit=1)[1])
                user: Record = await pool.fetchrow('''SELECT * from test.public."user" where nickname=$1''', nick, )
                if not user:
                    user: Record = await pool.fetchrow('''SELECT * from test.public."user" where username=$1''', nick, )
                    if not user:
                        nick = demojize(message.text.split(' ', maxsplit=1)[1])[1:]
                        user: Record = await pool.fetchrow('''SELECT * from test.public."user" where username=$1''',
                                                           nick, )
                        if not user:
                            nick = demojize(message.text.split(' ', maxsplit=1)[1])
                            user: Record = await pool.fetchrow(
                                '''SELECT id_user from test.public.nick_history where nick=$1''', nick, )
                            if user:
                                f_id = user[0]
                                user: Record = await pool.fetchrow('''SELECT * from test.public."user" where id=$1''',
                                                                   f_id, )
            if user:
                f_id = user[0]
                nick_h: Record = await pool.fetch('''SELECT nick,date from test.public.nick_history where id_user=$1''',
                                                  f_id, )
                ref: Record = await pool.fetch('''SELECT id_new_user from test.public.referals where id_refer=$1''',
                                               f_id, )
                race_ch: Record = await pool.fetch(
                    '''SELECT race_old,race_new,dat from test.public.race_change where id_user=$1''', f_id, )
                hosain: Record = await pool.fetchrow(
                    '''SELECT id_refer from test.public.referals where id_new_user=$1''', f_id, )
                if hosain:
                    hosain: Record = await pool.fetchrow(
                        '''SELECT guild,nickname,id from test.public."user" where id=$1''', hosain[0], )
                else:
                    hosain = ['', '', '']
        if user:
            nick_aws = ''
            for item in nick_h:
                nick_aws = f'{nick_aws}{item[0]}  {item[1]}\n'

            aws_race = ''
            for item in race_ch:
                aws_race = f'{aws_race}{race_convert.get(item[0])} <b>-></b> {race_convert.get(item[1])} ({item[2]})\n'

            aws_ref = ''
            for item in ref:
                aws_ref = f'{aws_ref}id: <code>{item[0]}</code>\n'

            await message.answer(
                emojize(f"""<b>Хозяин: {check_g(hosain[0])}</b><a href="tg://user?id={hosain[2]}">{emojize(hosain[1])}</a>
<b>:woman_genie:Раса</b> - {race_convert.get(user["race"])}
<b>:castle:Гильдия</b> - {user["guild"]}
<b>:clipboard:Ник</b> - {user["nickname"]}
<b>:sports_medal:Уровень</b> - {user["lvl"]}
<b>Ид</b> - <code>{user["id"]}</code>

<b>Профиль</b>
<a href="tg://user?id={user["id"]}">Тык </a> или @{user["username"]}  

<b>:clipboard:История смены ников</b>
{nick_aws}

<b>:woman_genie:История смены расы</b>
{aws_race}

<b>:alien:Рефералы</b>
{aws_ref}

"""))
        try:
            await message.bot.send_message(user["id"],
                                           f"[{emojize(who['guild'])}]<a href='tg://user?id={message.from_user.id}'>{emojize(who['nickname'])}</a>({message.from_user.id}) пробивает тебя через /get_user")
        except:
            pass
        if not user:
            await message.answer('Не смог никого найти')
    except:
        await message.answer(f'Команда использована не правильно.\n'
                             f'Пример - /get_user 156357128 (по ид)\n'
                             f'/get_user 🩸💉Eotanáis💉🩸  (или любой из ранее использованных ников)\n'
                             f'/get_user @VladimirTumanov или VladimirTumanov (по юзернейму)')
