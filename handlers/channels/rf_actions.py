from datetime import datetime

from aiogram import types
from aiogram.types.chat import ChatType
from aiogram.utils.emoji import demojize
from asyncpg import Connection, Record

from data.config import admins
from loader import dp, db
from utils.misc import rate_limit
import re

race_find = {':woman_astronaut:': 1, ':woman_elf:': 2, ':elf:‍:female_sign:': 2, ':robot:': 3}


def get_nick_in_str(text=''):
    tmp = text
    while tmp.count('(') != 0:
        tmp = tmp.split('(', maxsplit=1)[1]
    tmp = '(' + tmp
    return text.split(tmp)[0]


def get_guild_in_str(text=''):
    return text.split(']', maxsplit=1)[0][1:]


def get_nick_in_str_with_guild(text=''):
    text = text.split(']', maxsplit=1)[1]
    tmp = text
    while tmp.count('(') != 0:
        tmp = tmp.split('(', maxsplit=1)[1]
    tmp = '(' + tmp
    return text.split(tmp)[0]


def get_nick_in_str_with_lvl(text=''):
    tmp = text

    while tmp.count('(') != 1:
        tmp = tmp.split('(', maxsplit=1)[1]
    tmp = '(' + tmp

    return text.split(tmp)[0]


def get_id_in_str(text=''):
    while text.count('(') != 0:
        text = text.split('(', maxsplit=1)[1]
    return text[:-1]


async def req_db(f_id, f_nick, f_guild, f_race, f_lvl, last_a,
                 dat=datetime.strptime('2020-06-01 01:00:00.0000', '%Y-%m-%d %H:%M:%S.%f')):
    pool: Connection = db
    record: Record = await pool.fetchrow('''SELECT * FROM test.public.user WHERE id = $1''', f_id, )
    if not record:
        arg = f_id, f_nick, f_guild, f_race, f_lvl, dat, last_a
        await pool.fetch('''INSERT INTO test.public."user"(id,nickname,guild,race,lvl,date_update,last_activity) 
                            values ($1,$2,$3,$4,$5,$6,$7) ''', *arg)
        arg = f_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        await pool.fetch('''INSERT INTO test.public.totems(id_user, atk, atk_a, atk_b, atk_s, atk_g, def, def_a, def_b, 
                                                           def_s, def_g,  hp, hp_a, hp_b, hp_s, hp_g, dodge, dodge_a, 
                                                           dodge_b, dodge_s, dodge_g, crit, crit_a, crit_b, crit_s, 
                                                           crit_g, acc, acc_a, acc_b, acc_s, acc_g) 
                            values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,
                                    $24,$25,$26,$27,$28,$29,$30,$31)''', *arg)
        await pool.fetch('''INSERT INTO test.public.notify(id_user) values ($1)''', f_id, )
        await pool.fetch('''INSERT INTO test.public.top_conf(id_user) values ($1)''', f_id, )
    else:
        arg = f_id, f_nick, f_guild, f_race, f_lvl, last_a
        await pool.fetch('''UPDATE test.public.user SET nickname=$2,guild=$3,race=$4,lvl=$5,last_activity=$6 WHERE id=$1''', *arg)


async def db_new_nick(f_id, f_nick, f_race, dat, last_a):
    pool: Connection = db
    record: Record = await pool.fetchrow('''SELECT * FROM test.public.user WHERE id = $1''', f_id, )
    if not record:
        arg = f_id, f_nick, f_race, dat, last_a
        await pool.fetch('''INSERT INTO test.public."user"(id,nickname,race,date_update,last_activity) 
                            values ($1,$2,$3,$4,$5) ''', *arg)
        arg = f_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        await pool.fetch('''INSERT INTO test.public.totems(id_user, atk, atk_a, atk_b, atk_s, atk_g, def, def_a, def_b, 
                                                           def_s, def_g,  hp, hp_a, hp_b, hp_s, hp_g, dodge, dodge_a, 
                                                           dodge_b, dodge_s, dodge_g, crit, crit_a, crit_b, crit_s, 
                                                           crit_g, acc, acc_a, acc_b, acc_s, acc_g) 
                            values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,
                                    $24,$25,$26,$27,$28,$29,$30,$31)''', *arg)
        await pool.fetch('''INSERT INTO test.public.notify(id_user) values ($1)''', f_id, )
        await pool.fetch('''INSERT INTO test.public.top_conf(id_user) values ($1)''', f_id, )
        arg = f_id, dat, f_nick
        await pool.fetch('''INSERT INTO test.public.nick_history(id_user, date, nick) values ($1,$2,$3) ''', *arg)
    else:
        arg = f_id, dat, f_nick
        await pool.fetch('''INSERT INTO test.public.nick_history(id_user, date, nick) values ($1,$2,$3) ''', *arg)
        arg = f_id, f_nick
        await pool.fetch('''UPDATE test.public."user" SET nickname = $2 WHERE id = $1''', *arg)


async def db_new_refer(id_refer, id_new_user):
    pool: Connection = db
    arg = id_refer, id_new_user
    await pool.fetch('''INSERT INTO test.public.referals(id_new_user,id_refer) 
                                values ($1,$2)''', *arg)


async def db_race_change(f_id, race_old, race_new, dat):
    pool: Connection = db
    arg = f_id, race_old, race_new, dat
    await pool.fetch('''INSERT INTO test.public.race_change(id_user, race_old, race_new, dat) 
                                values ($1,$2,$3,$4)''', *arg)
    arg = f_id, race_new
    await pool.fetch('''UPDATE test.public."user" SET race = $2 WHERE id = $1''', *arg)

@rate_limit(0, 'rf_actions')
@dp.message_handler(user_id=admins, chat_type="private", commands='rf_actions', )
async def bot_command_rf_actions(message: types.Message):
    f_guild = None
    f_id = 0
    f_nick = 'a'
    f_race = 0
    f_lvl = 0
    msg = demojize(message.text).split(' ', maxsplit=1)[1]
    if msg.find('отправил') != -1 and msg.find('на склад гильдии') != -1:
        msg = msg.split('[:castle:] ', maxsplit=1)[1]
        for key in race_find:
            if msg.find(key) != -1:
                f_race = race_find[key]
                f_nick = get_nick_in_str_with_lvl(msg.split(key, maxsplit=1)[1].split(' отправил ')[0])
                f_guild = msg.split(f'на склад гильдии {key}')[1]
                f_lvl = msg.split('ур.)(')[0].split('(')[msg.split('ур.)(')[0].count('(')]
                f_id = msg.split('ур.)(')[1].split(')')[0]

        await req_db(int(f_id), f_nick, f_guild, f_race, int(f_lvl), datetime.now())
        await message.delete()
    elif msg.find('[:castle:] Гильдия') != -1 and msg.find(' отправила со склада') != -1:
        msg = msg.split('[:castle:] Гильдия ', maxsplit=1)[1]
        for key in race_find:
            if msg.find(key) != -1:
                f_race = race_find[key]
                f_nick = get_nick_in_str_with_lvl(msg.split(f' игроку {key}', maxsplit=1)[1])
                f_guild = msg.split(' отправила со склада ')[0].split(f'{key}')[1]
                tmp = msg.split(' игроку ')[1].split('ур.)(')[0]
                f_lvl = int(msg.split(' игроку ')[1].split('ур.)(')[0].split('(')[tmp.count('(')])
                f_id = int(msg.split(' игроку ')[1].split('ур.)(')[1].split(')')[0])

        await req_db(int(f_id), f_nick, f_guild, f_race, int(f_lvl), datetime.now())
        await message.delete()
    elif msg.find('[:circus_tent:] ') != -1 and msg.find(' купил у ') != -1:
        msg = msg.split('[:circus_tent:] ')[1]
        for item in msg.split(' купил у '):
            for key in race_find:
                if item.find(key) != -1:
                    f_race = race_find[key]
                    try:
                        f_nick = get_nick_in_str_with_guild(item.split(key)[1].split('.)(')[0])
                        f_guild = get_guild_in_str(item.split(key)[1].split('.)(')[0])
                        if len(f_nick) == 0:
                            f_guild = None
                            f_nick = get_nick_in_str(item.split(key)[1].split('.)(')[0])
                    except:
                        f_nick = get_nick_in_str(item.split(key)[1].split('.)(')[0])
                        f_guild = None
                    tmp = item.split('ур.)(')[0]
                    f_lvl = item.split('ур.)(')[0].split('(')[tmp.count('(')]
                    f_id = item.split('ур.)(')[1].split(')')[0]

            await req_db(int(f_id), f_nick, f_guild, f_race, int(f_lvl), datetime.now())
        await message.delete()
    elif msg.find(' пополнил банк ги ') != -1:
        msg = msg.split('[:castle:] ', maxsplit=1)[1]
        for key in race_find:
            if msg.find(key) != -1:
                f_race = race_find[key]
                f_nick = get_nick_in_str(msg.split(key)[1].split('.)(')[0])
                f_guild = msg.split(' пополнил банк ги ')[1].split(' на ')[0].split(key)[1]
                tmp = msg.split('ур.)(')[0]
                f_lvl = msg.split('ур.)(')[0].split('(')[tmp.count('(')]
                f_id = msg.split('ур.)(')[1].split(')')[0]

        await req_db(int(f_id), f_nick, f_guild, f_race, int(f_lvl), datetime.now())
        await message.delete()
    elif msg.find('[:castle:] Ги ') != -1:
        msg = msg.split('[:castle:] Ги ', maxsplit=1)[1]
        for key in race_find:
            if msg.find(key) != -1:
                f_race = race_find[key]
                f_nick = get_nick_in_str(msg.split('вывела персонажу ')[1].split(key)[1].split('.)(')[0])
                f_guild = msg.split(key)[1].split(' вывела персонажу ')[0]
                tmp = msg.split('ур.)(')[0]
                f_lvl = msg.split('ур.)(')[0].split('(')[tmp.count('(')]
                f_id = msg.split('ур.)(')[1].split(')')[0]

        await req_db(int(f_id), f_nick, f_guild, f_race, int(f_lvl), datetime.now())
        await message.delete()
    elif msg.find('[:clipboard:] Смена ника') != -1:
        msg = msg.split('[:clipboard:] Смена ника', maxsplit=1)[1]
        for key in race_find:
            if msg.find(key) != -1:
                f_race = race_find[key]
                f_nick = msg.split(key)[2]
                tmp = msg.split(key, maxsplit=1)[1].split(' на ник ')[0]
                f_id = msg.split(key, maxsplit=1)[1].split(' на ник ')[0].split('(')[tmp.count('(')][:-1]
        await db_new_nick(int(f_id), f_nick, f_race, message.date, datetime.now())
        await message.delete()
    elif msg.find('[:alien:] Регистрация ') != -1:
        msg = msg.split('[:alien:] Регистрация ', maxsplit=1)[1].split(' по рефке ')
        for item in msg:
            for key in race_find:
                if item.find(key) != -1:
                    f_race = race_find[key]
                    tmp = item.split(key, maxsplit=1)[1]
                    f_id = item.split(key, maxsplit=1)[1].split('(')[tmp.count('(')][:-1]
                    if msg.index(item) == 0:
                        id_refer = f_id
                        f_nick = item.split(key)[1].split('(')[0]
                        f_guild = None
                    else:
                        id_new_user = f_id
                        if (item.split(key)[1].find('[') != -1 and item.split(key)[1].find(']') != -1
                                and item.split(key)[1].split('(')[0].find(']') != len(
                                    item.split(key)[1].split('(')[0]) - 1):
                            f_nick = item.split(key)[1].split('(')[0].split(']', maxsplit=1)[1]
                            f_guild = item.split(key)[1].split('[')[1].split(']', maxsplit=1)[0]
                        else:
                            f_nick = item.split(key)[1].split('(')[0]
                            f_guild = None

                    await req_db(int(f_id), f_nick, f_guild, f_race, 0, message.date)
        await db_new_refer(int(id_refer), int(id_new_user))
        await message.delete()
    elif msg.find('[:woman_genie:] Смена расы ') != -1 or msg.find(
            '[:genie:‍:female_sign:] Смена расы') != -1 or msg.find('[:woman_genie_selector:] Смена расы') != -1:
        msg = msg.split('Смена расы ', maxsplit=1)[1]
        for key in race_find:
            if msg.split(' на расу ')[0].find(key) != -1:
                f_id = get_id_in_str(msg.split(' на расу ')[0].split(key)[0][:-1])
        msg = msg.split(' на расу ')
        for item in msg:
            for key in race_find:
                if item.find(key) != -1:
                    if msg.index(item) == 0:
                        race_old = race_find[key]
                    elif msg.index(item) == 1:
                        race_new = race_find[key]
        await db_race_change(int(f_id), int(race_old), int(race_new), message.date)
        await message.delete()
    elif msg.find('[:fountain:] ') != -1 and msg.find('закончил выработку') != -1:
        msg2 = msg.split('[:fountain:] ')[1]
        msg = [msg2.split(' закончил выработку')[0], msg2.split('ед. для ')[1].split(' за :')[0]]
        for item in msg:
            for key in race_find:
                if item.find(key) != -1:
                    f_race = race_find[key]
                    try:
                        f_nick = get_nick_in_str_with_guild(re.split(r' \d\dур.\(\d+', item.split(key)[1])[0])
                        f_guild = get_guild_in_str(re.split(r' \d\dур.\(\d+', item.split(key)[1])[0])
                        if len(f_nick) == 0:
                            f_guild = None
                            f_nick = get_nick_in_str(re.split(r' \d\dур.\(\d+', item.split(key)[1])[0])
                    except:
                        f_nick = get_nick_in_str(re.split(r' \d\dур.\(\d+', item.split(key)[1])[0])
                        f_guild = None
                    f_lvl = re.findall(r'(\d\d)ур.', item)[0]   #item.split('ур.)(')[0].split('(')[tmp.count('(')]
                    f_id = re.findall(r'ур.\((\d+)\)', item)[0] #item.split('ур.)(')[1].split(')')[0]

            await req_db(int(f_id), f_nick, f_guild, f_race, int(f_lvl), datetime.now())
        await message.delete()
    else:
        pass
