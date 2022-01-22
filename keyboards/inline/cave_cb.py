from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime


dat_cave = CallbackData('caves', 'action','id','date')

async def create_cb_cave(id, date,lvl):
    kb = InlineKeyboardMarkup(row_width=1)
    if lvl == 1:
        kb_update = InlineKeyboardButton('🔄 Обновить', callback_data=dat_cave.new('update_cave_lvl',str(id),str(date).replace(':',';')))
        view_change = InlineKeyboardButton('🥇🥈🥉 Показать всех', callback_data=dat_cave.new('update_cave_any',str(id),str(date).replace(':',';')))
    else:
        kb_update = InlineKeyboardButton('🔄 Обновить', callback_data=dat_cave.new('update_cave_any',str(id),str(date).replace(':',';')))
        view_change = InlineKeyboardButton('🏅 Показать свою лигу', callback_data=dat_cave.new('update_cave_lvl',str(id),str(date).replace(':',';')))

    kb.add(kb_update)
    kb.add(view_change)
    return kb

async def upd_cave_btn(id):
    pool: Connection = db

    list_cave = []
    sort_cave_lvl = await pool.fetchval('''SELECT lvl from test.public."user" where id=$1''', id,)
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

    ch = 1
    for item in list_cave:
        res_cave = f'{res_cave}<b>{ch})</b>{item}\n'
        ch += 1

    res_cave = f'{res_cave}\n'

    res_cave = res_cave + 'Показать всех - /cave_all'
    return emojize(res_cave)



async def upd_cave_btn_all():
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
        return emojize(res_cave)
    else:
        return emojize('В пещерах сейчас пусто')



@dp.callback_query_handler(dat_cave.filter(action=['update_cave_lvl', 'update_cave_any']))
async def inline_kb_update_cave_callback_handler(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):

        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                if callback_data["action"] == 'update_cave_lvl':
                    anw_txt = await upd_cave_btn(int(callback_data["id"]))
                    await query.bot.edit_message_text(text=anw_txt,
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_cave(callback_data["id"],callback_data_time,1))
                elif callback_data["action"] == 'update_cave_any':
                    anw_txt = await upd_cave_btn_all()
                    await query.bot.edit_message_text(text=anw_txt,
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_cave(callback_data["id"],callback_data_time,0))
                await query.answer(emojize(':check_mark_button:Обновлено!'), cache_time=5)
            except:
                await query.answer(emojize(':check_mark_button:Обновлено!'), cache_time=5)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=5)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /cave или /cave_all для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)
