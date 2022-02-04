from aiogram import types
from loader import dp, db
from aiogram.types.chat import ChatType
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import demojize,emojize
from data.config import admins
from utils.misc import rate_limit



race_convert = {1: ':woman_astronaut: Basilaris', 2: ':woman_elf: Castitas', 3: ':robot: Aquilla'}


@rate_limit(3, 'me')
@dp.message_handler(commands='me')
async def bot_command_get_user(message: types.Message):
    pool: Connection = db
    user: Record = await pool.fetchrow('''SELECT * from test.public."user" where id=$1''', message.from_user.id,)
    if user:
        nick_h: Record = await pool.fetch('''SELECT nick,date from test.public.nick_history where id_user=$1''', message.from_user.id,)
        ref: Record = await pool.fetch('''SELECT id_new_user from test.public.referals where id_refer=$1''', message.from_user.id,)
        race_ch: Record = await pool.fetch('''SELECT race_old,race_new,dat from test.public.race_change where id_user=$1''', message.from_user.id,)
        totems: Record = await pool.fetchrow('''SELECT atk,acc,def,crit,dodge,hp from test.public.totems where id_user=$1''', message.from_user.id,)
        nick_aws = ''
        hosain: Record = await pool.fetchrow('''SELECT id_refer from test.public.referals where id_new_user=$1''', message.from_user.id,)
        if hosain:
            hosain: Record = await pool.fetchrow('''SELECT guild,nickname,id from test.public."user" where id=$1''', hosain[0],)
        else:
            hosain = ['','','']
        for item in nick_h:
            nick_aws = f'{nick_aws}{item[0]}  {item[1]}\n'

        aws_race = ''
        for item in race_ch:
            aws_race = f'{aws_race}{race_convert.get(item[0])} <b>-></b> {race_convert.get(item[1])} ({item[2]})\n'

        aws_ref = ''
        for item in ref:
            aws_ref = f'{aws_ref}id: <code>{item[0]}</code>\n'

        await message.answer(emojize(f"""<b>Хозяин: [{emojize(hosain[0])}]</b><a href="tg://user?id={hosain[2]}">{emojize(hosain[1])}</a>
<b>:woman_genie:Раса</b> - {race_convert.get(user["race"])}            
<b>:castle:Гильдия</b> - {user["guild"]}
<b>:clipboard:Ник</b> - {user["nickname"]}
<b>:sports_medal:Уровень</b> - {user["lvl"]} (:puzzle_piece:{user["paragon"]})
<b>Ид</b> - <code>{user["id"]}</code>

<b>Статы</b> 
:red_heart:{int(user["hp"])} :crossed_swords:{int(user["atk"])} :shield:{int(user["def"])}
:dashing_away:{user["dodge"]:.2f} :bullseye:{user["crit"]:.2f} :hourglass_not_done:{user["accuracy"]:.2f}

<b>Тотемы (/totems)</b> 
:dagger:{totems["atk"]} :water_wave:{totems["def"]} :comet:{totems["hp"]}
:flexed_biceps_medium-light_skin_tone:{totems["dodge"]} :hourglass_not_done:{totems["acc"]} :high_voltage:{totems["crit"]}

<b>Профиль</b>
<a href="tg://user?id={user["id"]}">Тык </a> или @{user["username"]}  

Уведомления - /config
Рейтинг ежедневок - /daily

<b>:clipboard:История смены ников</b>
{nick_aws}

<b>:woman_genie:История смены расы</b>
{aws_race}

<b>:alien:Рефералы</b>
{aws_ref}"""))
    else:
        await message.answer('Я не знаю тебя')
