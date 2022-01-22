import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record
from filters.guild_check import check_g
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData


dat_c_inv= CallbackData('cave_cr', 'action', 'id', 'lvl', 'c_id')


async def create_cb_cave_lvl(id: int, lvl: str, cave_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(InlineKeyboardButton('🎭 Пригласить', callback_data=dat_c_inv.new('cave_inv', str(id), lvl, cave_id)))
    kb.add(InlineKeyboardButton('🏅 Выбрать диапазон', callback_data=dat_c_inv.new('cave_d', str(id), lvl, cave_id)))
    kb.add(InlineKeyboardButton('🎭 Вступить', url=f'http://t.me/share/url?url=/group_guild_join_{cave_id}'),
           InlineKeyboardButton('❌ Выйти', url='http://t.me/share/url?url=❌Выйти из группы'))
    return kb


@dp.callback_query_handler(dat_c_inv.filter(action=['cave_inv', 'cave_d']))
async def inline_kb_cr_cave_inv(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        list_bad = []
        inv_true = 0
        pool: Connection = db
        usr: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', int(callback_data["id"]),)
        if callback_data['action'] == 'cave_inv':
            arg = usr["guild"], usr["id"], int(callback_data["lvl"].split('-')[0]), int(callback_data["lvl"].split('-')[1])
            all_user: Record = await pool.fetch('''select * from test.public."user" c 
            join test.public.notify n on c.id = n.id_user 
            where guild=$1 and c.user_dialog = true and n.caves = true and c.id <>$2 and c.lvl>=$3 and c.lvl<=$4''', *arg)
            if all_user:
                for inv in all_user:
                    try:
                        await query.bot.send_message(
                            chat_id=inv["id"],
                            text=(f'{check_g(usr["guild"])}<a href="tg://user?id={usr["id"]}">{emojize(usr["nickname"])}</a> приглашает тебя в 🚠пещеры\nЛига 🏅{callback_data["lvl"]}\n'
                                  f'<a href="http://t.me/share/url?url=/group_guild_join_{callback_data["с_id"]}">/group_guild_join_{callback_data["с_id"]}</a>'),
                            reply_markup=await create_cb_cave_inv_send(callback_data["с_id"]))
                        await asyncio.sleep(.07)
                        inv_true += 1
                    except:
                        list_bad.append(inv["id"])
                anw_txt = (f'Привет {check_g(usr["guild"])}{emojize(usr["nickname"])}\n'
                           f'Ты создал группу в 🚠пещеры для лиги 🏅{callback_data["lvl"]}\n\n'
                           f'Приглашения высланы! ({inv_true})')
                await query.bot.edit_message_text(text=anw_txt,
                                                  chat_id=query.message.chat.id,
                                                  message_id=query.message.message_id,
                                                  reply_markup=await create_cb_cave_inv_send(
                                                      callback_data["c_id"]
                                                  ))
                if list_bad:
                    for bad_id in list_bad:
                        await pool.fetchval('''UPDATE test.public."user" SET user_dialog=false WHERE id=$1''', int(bad_id))
        elif callback_data['action'] == 'cave_d':
            anw_txt = (f'Привет {check_g(usr["guild"])}{emojize(usr["nickname"])}\n'
                       f'Ты создал группу в 🚠пещеру для лиги 🏅{callback_data["lvl"]}\n\n'
                       f'Выбери 🏅лигу, которой нужно прислать приглашения -> ')
            await query.bot.edit_message_text(text=anw_txt,
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id,
                                              reply_markup=await create_cb_sel_l_cave(
                                                  callback_data["id"],
                                                  callback_data["c_id"]
                                              ))
        await query.answer(emojize(':check_mark_button:Обновлено!'), cache_time=5)
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)


dat_c_sel_l = CallbackData('cave_cr', 'action', 'id', 'lvl', 'c_id')


async def create_cb_sel_l_cave(id: int, cave_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(InlineKeyboardButton('Всем', callback_data=dat_c_sel_l.new('inv',str(id),'40-60',cave_id)))
    kb.add(InlineKeyboardButton('40-44', callback_data=dat_c_sel_l.new('inv',str(id),'40-44',cave_id)),
           InlineKeyboardButton('45-48', callback_data=dat_c_sel_l.new('inv',str(id),'45-48',cave_id)),
           InlineKeyboardButton('49-49', callback_data=dat_c_sel_l.new('inv',str(id),'49-49',cave_id)))
    kb.add(InlineKeyboardButton('50-50', callback_data=dat_c_sel_l.new('inv',str(id),'50-50',cave_id)),
           InlineKeyboardButton('51-52', callback_data=dat_c_sel_l.new('inv',str(id),'51-52',cave_id)),
           InlineKeyboardButton('53-54', callback_data=dat_c_sel_l.new('inv',str(id),'53-54',cave_id)))
    kb.add(InlineKeyboardButton('55-55', callback_data=dat_c_sel_l.new('inv',str(id),'55-55',cave_id)),
           InlineKeyboardButton('56-57', callback_data=dat_c_sel_l.new('inv',str(id),'56-57',cave_id)),
           InlineKeyboardButton('58-59', callback_data=dat_c_sel_l.new('inv',str(id),'58-59',cave_id)))
    kb.add(InlineKeyboardButton('60-60', callback_data=dat_c_sel_l.new('inv',str(id),'60-60',cave_id)))
    return kb


async def create_cb_cave_inv_send(cave_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton('🎭 Вступить', url=f'http://t.me/share/url?url=/group_guild_join_{cave_id}'),
           InlineKeyboardButton('❌ Выйти', url='http://t.me/share/url?url=❌Выйти из группы'))
    return kb


@dp.callback_query_handler(dat_c_sel_l.filter(action=['inv']))
async def inline_kb_cr_send_inv_chose(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        list_bad = []
        pool: Connection = db
        usr: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', int(callback_data["id"]),)
        arg = usr["guild"], usr["id"], int(callback_data["lvl"].split('-')[0]), int(callback_data["lvl"].split('-')[1])
        all_user: Record = await pool.fetch('''select * from test.public."user" c 
            join test.public.notify n on c.id = n.id_user 
            where guild=$1 and c.user_dialog = true and n.caves = true and c.id <>$2 and c.lvl>=$3 and c.lvl<=$4''', *arg)
        if all_user:
            leg = [
                '40-44', '45-48', '49-49', '50-50', '51-52',
                '53-54', '55-55', '56-57', '58-59', '60-60'
            ]
            usr_leg = ''
            for item in leg:
                if int(item.split('-')[0]) >= usr["lvl"]:
                    if int(item.split('-')[1]) <= int(item.split('-')[1]):
                        usr_leg = item
                        break
            inv_true = 0
            for inv in all_user:
                try:
                    await query.bot.send_message(
                        chat_id=inv["id"],
                        text=(f'{check_g(usr["guild"])}<a href="tg://user?id={usr["id"]}">{emojize(usr["nickname"])}</a> приглашает тебя в 🚠пещеры\nЛига 🏅{usr_leg}\n'
                              f'<a href="http://t.me/share/url?url=/group_guild_join_{callback_data["с_id"]}">/group_guild_join_{callback_data["с_id"]}</a>'),
                        reply_markup=await create_cb_cave_inv_send(callback_data["с_id"]))
                    await asyncio.sleep(.07)
                    inv_true += 1
                except:
                    list_bad.append(inv["id"])
            anw_txt = (f'Привет {check_g(usr["guild"])}{emojize(usr["nickname"])}\n'
                       f'Ты создал группу в 🚠пещеры для лиги 🏅{usr_leg}\n\n'
                       f'Приглашения для 🏅{callback_data["lvl"]} высланы! ({inv_true})')
            await query.bot.edit_message_text(text=anw_txt,
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id,
                                              reply_markup=await create_cb_cave_inv_send(
                                                  callback_data["c_id"]
                                                  ))
            if list_bad:
                for bad_id in list_bad:
                    await pool.fetchval('''UPDATE test.public."user" SET user_dialog=false WHERE id=$1''', int(bad_id))
        await query.answer(emojize(':check_mark_button:Обновлено!'), cache_time=5)
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)

