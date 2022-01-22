from aiogram import types

from keyboards.inline.cave_cb import create_cb_cave
from loader import dp, db
from aiogram.types.chat import ChatType
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import emojize
from data.config import admins
from utils.misc import rate_limit

race_find = {':woman_astronaut:': 1, ':woman_elf:': 2, ':elf:‍:female_sign:': 2, ':robot:': 3}


@rate_limit(2, 'cave')
@dp.message_handler(commands='cave')
async def bot_command_rf_caves(message: types.Message):
    pool: Connection = db

    list_cave = []
    sort_cave_lvl = await pool.fetchval('''SELECT lvl from test.public."user" where id=$1''', message.from_user.id,)
    cave_all: Record = await pool.fetch('''SELECT * from test.public.caves''')
    for item in cave_all:
        total_p = ''
        t_start = (datetime.now() - item[2]).seconds // 60
        if item[3] != '':
            dt_now = datetime.now()

            if (dt_now - item[3]).seconds < 60 * 8:
                p_min = str(7 - ((dt_now - item[3]).seconds // 60)) + 'м '

                p_sec = str(((60 * 7 - (dt_now - item[3]).seconds) - ((60 * 8 - (dt_now - item[3]).seconds) // 60 + 1) * 60) % 60) + 'c'
                total_p = f' :shield:{p_min}{p_sec}'
        if sort_cave_lvl >= int(item[9].split('-')[0]) and sort_cave_lvl <= int(item[9].split('-')[1]):
            list_cave.append(f'[{item[5]}]{item[4]}<a href="tg://user?id={item[12]}">{item[1]}</a>(:hourglass_done:{t_start}м{total_p})'
                             f'<b>[:crossed_swords:{item[6]}:handshake:{item[8]}:skull_and_crossbones:{item[7]}</b>]')


    def keyFunc(item):
        return int(item.split('(:hourglass_done:', maxsplit=1)[1].split('м', maxsplit=1)[0])

    list_cave.sort(key=keyFunc, reverse=True)

    if sort_cave_lvl < 45:
        res_cave = '<b>Лига 40-44:sports_medal:</b>\n'
    elif sort_cave_lvl > 44 and sort_cave_lvl < 49:
        res_cave = '<b>Лига 45-48:sports_medal:</b>\n'
    elif sort_cave_lvl == 49:
        res_cave = '<b>Лига 49-49:sports_medal:</b>\n'
    elif sort_cave_lvl == 50:
        res_cave = '<b>Лига 50-50:sports_medal:</b>\n'
    elif sort_cave_lvl > 50 and sort_cave_lvl < 53:
        res_cave = '<b>Лига 51-52:sports_medal:</b>\n'
    elif sort_cave_lvl > 52 and sort_cave_lvl < 55:
        res_cave = '<b>Лига 53-54:sports_medal:</b>\n'
    elif sort_cave_lvl == 55:
        res_cave = '<b>Лига 55:sports_medal:</b>\n'
    elif sort_cave_lvl > 55 and sort_cave_lvl < 58:
        res_cave = '<b>Лига 56-57:sports_medal:</b>\n'
    elif sort_cave_lvl > 57 and sort_cave_lvl < 60:
        res_cave = '<b>Лига 58-59:sports_medal:</b>\n'
    elif sort_cave_lvl > 59:
        res_cave = '<b>Лига 60:sports_medal:</b>\n'
    if not res_cave:
        res_cave = ''
    ch = 1
    for item in list_cave:
        res_cave = f'{res_cave}<b>{ch})</b>{item}\n'
        ch += 1

    res_cave = f'{res_cave}\n'

    res_cave = res_cave + 'Показать всех - /cave_all'
    if len(list_cave) > 0:
        await message.reply(emojize(res_cave), reply_markup=await create_cb_cave(message.from_user.id, message.date,1))
    else:
        await message.reply('В пещерах сейчас пусто\n\nПоказать всех - /cave_all', reply_markup=await create_cb_cave(message.from_user.id, message.date,1))


