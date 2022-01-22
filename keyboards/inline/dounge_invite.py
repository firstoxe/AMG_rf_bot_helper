import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record

from filters.guild_check import check_g
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime

DOUNGE_NAME = {'1-5': '🗝 Канализация Ген.Штаба(1-5)',
               '6-10': '🗝 Рудник у Аванпоста(6-10)',
               '11-15': '🗝 Забытая пещера(11-15)',
               '16-20': '🗝 Покинутый терминал(16-20)',
               '21-25': '🗝 Сбитый челнок(21-25)',
               '26-30': '🗝 Кровавый лабиринт(26-30)',
               '31-35': '🗝 Пустынный шпиль(31-35)',
               '36-40': '🗝 Логово Псевдодракона(36-40)',
               '41-45': '🗝 Пещера "Церберус"(41-45)',
               '46-50': '🗝 Воздушная крепость(46-50)',
               '51-55': '🗝 Лаборатория "Картелла"(51-55)',
               '56-60': '🗝 Крепость культистов (56-60)'
               }

dat_d_lvl = CallbackData('dounge_cr', 'action', 'id', 'lvl', 'd_id')


async def create_cb_dounge_lvl(id: int, lvl: int, dounge_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=3)
    c = 1
    ch = 0
    list_kb = []
    while c < lvl:
        list_kb.append(
            InlineKeyboardButton(
                str(c)+'-'+str(c+4),
                callback_data=dat_d_lvl.new(
                    'lvl',
                    str(id),
                    str(c)+'-'+str(c+4),
                    dounge_id
                )
            )
        )
        ch += 1
        c += 5
        if ch == 3:
            kb.add(*list_kb)
            list_kb = []
            ch = 0
    if len(list_kb) > 0:
        kb.add(*list_kb)
    return kb


@dp.callback_query_handler(dat_d_lvl.filter(action=['lvl']))
async def inline_kb_cr_dounge_lvl(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        pool: Connection = db
        usr: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', int(callback_data["id"]),)
        anw_txt = (f'Привет {check_g(usr["guild"])}<a href="tg://user?id={usr["id"]}">{emojize(usr["nickname"])}</a>\n'
                   f'Данж {DOUNGE_NAME[callback_data["lvl"]]}\n'
                   f'Цена входа в ключах: ')
        await query.bot.edit_message_text(text=anw_txt,
                                          chat_id=query.message.chat.id,
                                          message_id=query.message.message_id,
                                          reply_markup=await create_cb_dounge_price(
                                              callback_data["id"],
                                              callback_data["lvl"],
                                              callback_data["d_id"]
                                          ))
        await query.answer(emojize(':check_mark_button:Обновлено!'), cache_time=5)
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)


async def create_cb_dounge_price(id: int, lvl: int, dounge_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(InlineKeyboardButton('Бесплатно', callback_data=dat_d_lvl.new('lvl_0',str(id),lvl,dounge_id)))
    kb.add(InlineKeyboardButton('1 ключ', callback_data=dat_d_lvl.new('lvl_1',str(id),lvl,dounge_id)),
           InlineKeyboardButton('2 ключа', callback_data=dat_d_lvl.new('lvl_2',str(id),lvl,dounge_id)),
           InlineKeyboardButton('3 ключа', callback_data=dat_d_lvl.new('lvl_3',str(id),lvl,dounge_id)))
    kb.add(InlineKeyboardButton('4 ключа', callback_data=dat_d_lvl.new('lvl_4',str(id),lvl,dounge_id)),
           InlineKeyboardButton('5 ключей', callback_data=dat_d_lvl.new('lvl_5',str(id),lvl,dounge_id)),
           InlineKeyboardButton('6 ключей', callback_data=dat_d_lvl.new('lvl_6',str(id),lvl,dounge_id)))
    kb.add(InlineKeyboardButton('> 6 ключей', callback_data=dat_d_lvl.new('lvl_7',str(id),lvl,dounge_id)))
    return kb


@dp.callback_query_handler(dat_d_lvl.filter(action=['lvl_0','lvl_1', 'lvl_2', 'lvl_3', 'lvl_4', 'lvl_5', 'lvl_6', 'lvl_7']))
async def inline_kb_cr_dounge_price(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        pool: Connection = db
        usr: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', int(callback_data["id"]),)
        anw_txt = (f'Привет {check_g(usr["guild"])}<a href="tg://user?id={usr["id"]}">{emojize(usr["nickname"])}</a>\n'
                   f'Данж {DOUNGE_NAME[callback_data["lvl"]]}\n'
                   f'Цена входа 🗝 -> '
                   f'{"Бесплатно" if callback_data["action"] == "lvl_0" else "> 6 ключей" if callback_data["action"] == "lvl_7" else callback_data["action"].split("lvl_")[1]}\n'
                   f'Кому выслать приглашения?')
        await query.bot.edit_message_text(text=anw_txt,
                                          chat_id=query.message.chat.id,
                                          message_id=query.message.message_id,
                                          reply_markup=await create_cb_dounge_invite(
                                              callback_data["id"],
                                              callback_data["lvl"],
                                              callback_data["d_id"],
                                              callback_data["action"].split("lvl_")[1]
                                          ))
        await query.answer(emojize(':check_mark_button:Обновлено!'), cache_time=5)
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)


dat_d_invite = CallbackData('dounge_invite', 'action', 'id', 'lvl', 'd_id', 'price')


async def create_cb_dounge_invite(id: str, lvl: str, dounge_id: str, price: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    pool: Connection = db
    usr: Record = await pool.fetchval('''SELECT guild FROM test.public."user" WHERE id = $1''', int(id),)
    kb.add(InlineKeyboardButton(emojize(usr), callback_data=dat_d_invite.new('guild', str(id),lvl,dounge_id,price)),
           InlineKeyboardButton('Всем', callback_data=dat_d_invite.new('all',str(id),lvl,dounge_id,price)))
    kb.add(InlineKeyboardButton('Пропустить', callback_data=dat_d_invite.new('none',str(id),lvl,dounge_id,price)))
    return kb


@dp.callback_query_handler(dat_d_invite.filter(action=['guild', 'all', 'none']))
async def inline_kb_cr_send_invite(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        list_bad = []
        all_user = []
        pool: Connection = db
        usr: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', int(callback_data["id"]),)
        anw_txt = (f'Привет {check_g(usr["guild"])}<a href="tg://user?id={usr["id"]}">{emojize(usr["nickname"])}</a>\n'
                   f'Данж {DOUNGE_NAME[callback_data["lvl"]]}\n'
                   f'Цена входа 🗝 -> '
                   f'{"Бесплатно" if callback_data["price"] == "0" else "> 6 ключей" if callback_data["price"] == "7" else callback_data["price"]}\n')
        if callback_data["action"] == 'guild':
            arg = usr["guild"], usr["id"], int(callback_data["lvl"].split('-')[0]), int(callback_data["lvl"].split('-')[1])
            all_user: Record = await pool.fetch('''select * from test.public."user" c 
            join test.public.notify n on c.id = n.id_user 
            where guild=$1 and c.user_dialog = true and n.dounge_guild = true and c.id <>$2 and c.lvl>=$3 and c.lvl<=$4''', *arg)
        elif callback_data["action"] == 'all':
            arg = usr["race"], usr["id"], int(callback_data["lvl"].split('-')[0]), int(callback_data["lvl"].split('-')[1])
            all_user: Record = await pool.fetch('''select * from test.public."user" c 
            join test.public.notify n on c.id = n.id_user 
            where race=$1 and c.user_dialog = true and n.dounge = true and c.id <>$2 and c.lvl>=$3 and c.lvl<=$4''', *arg)
        if callback_data["action"] != 'none' and all_user:
            inv_true = 0
            for inv in all_user:
                try:
                    await query.bot.send_message(
                        chat_id=inv["id"],
                        text=(f'{check_g(usr["guild"])}<a href="tg://user?id={usr["id"]}">{emojize(usr["nickname"])}</a> приглашает тебя в данж {DOUNGE_NAME[callback_data["lvl"]]}\n'
                              f'<a href="http://t.me/share/url?url=/group_join_{callback_data["d_id"]}">/group_join_{callback_data["d_id"]}</a>'),
                        reply_markup=await create_cb_dounge_cr_link(f'http://t.me/share/url?url=/group_join_{callback_data["d_id"]}'))
                    await asyncio.sleep(.07)
                    inv_true += 1
                except:
                    list_bad.append(inv["id"])
            anw_txt = f'{anw_txt}\nПриглашения высланы ({inv_true})'
            await query.bot.edit_message_text(text=anw_txt,
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id,
                                              reply_markup=await create_cb_dounge_cr_link(f'http://t.me/share/url?url=/group_join_{callback_data["d_id"]}'))
        else:
            await query.bot.edit_message_text(text=anw_txt,
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id,
                                              reply_markup=await create_cb_dounge_cr_link(f'http://t.me/share/url?url=/group_join_{callback_data["d_id"]}'))
        await query.answer(emojize(':check_mark_button:Обновлено!'), cache_time=5)
        if list_bad:
            for bad_id in list_bad:
                await pool.fetchval('''UPDATE test.public."user" SET user_dialog=false WHERE id=$1''', int(bad_id))
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)


async def create_cb_dounge_cr_link(url: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton('🎭 Вступить', url=url),
           InlineKeyboardButton('❌ Выйти', url='http://t.me/share/url?url=/exit_group'))
    return kb