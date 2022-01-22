from datetime import datetime

from aiogram import types
from aiogram.types.chat import ChatType
from aiogram.utils.emoji import emojize
from asyncpg import Connection, Record

from data.config import admins
from keyboards.inline.cave_cb import create_cb_cave
from loader import dp, db
from utils.misc import rate_limit

race_find = {':woman_astronaut:': 1, ':woman_elf:': 2, ':elf:‍:female_sign:': 2, ':robot:': 3}


@rate_limit(2, 'cave_all')
@dp.message_handler(commands='cave_all')
async def bot_command_rf_caves_all(message: types.Message):
    pool: Connection = db
    list_cave = []
    cave_all: Record = await pool.fetch('''SELECT * from test.public.caves''')
    for item in cave_all:
        total_p = ''
        t_start = (datetime.now() - item[2]).seconds // 60
        if item[3] != '':
            dt_now = datetime.now()
            if (dt_now - item[3]).seconds < 60 * 8:
                p_min = str(7 - ((dt_now - item[3]).seconds // 60)) + 'м '

                p_sec = str(((60 * 7 - (dt_now - item[3]).seconds) - (
                            (60 * 8 - (dt_now - item[3]).seconds) // 60 + 1) * 60) % 60) + 'c'
                total_p = f' :shield:{p_min}{p_sec}'
        list_cave.append(
            f'[{item[5]}]{item[4]}<a href="tg://user?id={item[12]}">{item[1]}</a>(:hourglass_done:{t_start}м{total_p})'
            f'<b>[:crossed_swords:{item[6]}:handshake:{item[8]}:skull_and_crossbones:{item[7]}</b>]|||{item[9]}')

    def keyFunc(item):
        return int(item.split('(:hourglass_done:', maxsplit=1)[1].split('м', maxsplit=1)[0])

    list_cave.sort(key=keyFunc, reverse=True)

    mega_list = {}
    for item in list_cave:
        if len(mega_list) > 0:
            try:
                var_ls = mega_list.get(item.split('|||', maxsplit=1)[1])
                var_ls.append(item.split('|||')[0])
                mega_list.update({item.split('|||', maxsplit=1)[1]: var_ls})
            except:
                mega_list.update({item.split('|||', maxsplit=1)[1]: [item.split('|||')[0]]})
        else:

            mega_list.update(
                {item.split('|||', maxsplit=1)[1]: [item.split('|||')[0]]})

    res_cave = ''
    for item in mega_list:
        res_cave = f'{res_cave}<b>Лига {item}:sports_medal:</b>\n'
        lvl_ch = 1
        for item2 in mega_list.get(item):
            res_cave = f'{res_cave}<b>{lvl_ch})</b>{item2}\n'
            lvl_ch += 1
        res_cave = f'{res_cave}\n'

    res_cave = res_cave + 'Показать лигу по уровню - /cave'
    if len(cave_all) > 0:
        await message.reply(emojize(res_cave), reply_markup=await create_cb_cave(message.from_user.id, message.date,0))
    else:
        await message.reply('В пещерах сейчас пусто', reply_markup=await create_cb_cave(message.from_user.id, message.date,0))
