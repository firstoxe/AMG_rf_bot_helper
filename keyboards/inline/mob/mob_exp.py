from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record

from handlers.commands.mob_fight_all import mob_figth
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime


dat_mob_loc_ex = CallbackData('mob_exp', 'action', 'id', 'date', 'lvl_mob')

async def create_cb_mob_loc_exp_lvl(id, date, diapason):
    kb = InlineKeyboardMarkup(row_width=3)
    diapason_start = int(diapason.split('-')[0])
    diapason_end = int(diapason.split('-')[1])
    ch = 1
    list_kb = []
    while diapason_start <= diapason_end:
        if ch != 4 and ch <= diapason_end:
            list_kb.append(InlineKeyboardButton(str(diapason_start), callback_data=dat_mob_loc_ex.new('figth',str(id),str(date).replace(':',';'),str(diapason_start))))
            ch += 1
            diapason_start += 1
        else:
            kb.add(*list_kb)
            list_kb = []
            ch = 1
    if len(list_kb)>0:
        kb.add(*list_kb)
    kb.add(InlineKeyboardButton('🔙 Назад', callback_data=dat_mob_loc_ex.new('BackLoc',str(id),str(date).replace(':',';'), 0)))
    return kb

dat_mob_loc_ex_retry = CallbackData('mob_exp_figth', 'action', 'id', 'date', 'lvl_mob')

async def create_cb_mob_loc_exp_fight(id, date, mob):
    kb1 = InlineKeyboardMarkup(row_width=1)
    kb1.add(InlineKeyboardButton('🔄 Обновить', callback_data=dat_mob_loc_ex_retry.new('figth_mob', str(id), str(date).replace(':',';'), str(mob))))
    kb1.add(InlineKeyboardButton('🔙 Назад', callback_data=dat_mob_loc_ex_retry.new('BackLocList',str(id),str(date).replace(':',';'), str(mob))))
    return kb1


@dp.callback_query_handler(dat_mob_loc_ex.filter(action=['BackLoc']))
async def inline_kb_mob_loc_exp_back1(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            from .mob_loc import create_cb_mob_loc_exp
            await query.bot.edit_message_text(text='Выбери локацию',
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id,
                                              reply_markup=await create_cb_mob_loc_exp(callback_data["id"],callback_data_time))
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)


@dp.callback_query_handler(dat_mob_loc_ex.filter(action=['figth']))
async def inline_kb_mob_loc_exp_figth1(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            await query.bot.edit_message_text(text=await mob_figth(callback_data["lvl_mob"], int(callback_data["id"]), 'loc'),
                                                  message_id=query.message.message_id,
                                                  chat_id=query.message.chat.id,
                                                  reply_markup=await create_cb_mob_loc_exp_fight(callback_data["id"],callback_data_time, callback_data["lvl_mob"]))
            await query.answer(cache_time=3)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)


@dp.callback_query_handler(dat_mob_loc_ex_retry.filter(action=['BackLocList']))
async def inline_kb_mob_loc_exp_back2(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            if int(callback_data["lvl_mob"]) < 11:
                lvl_loc = '2-10'
            elif int(callback_data["lvl_mob"]) > 50:
                lvl_loc = '51-60'
            else:
                lvl_loc = str(divmod(int(callback_data["lvl_mob"]), 10)[0]*10+1)+'-'+str(divmod(int(callback_data["lvl_mob"]), 10)[0]*10+10)
            await query.bot.edit_message_text(text='Выбери уровень моба 👹',
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id,
                                              reply_markup=await create_cb_mob_loc_exp_lvl(callback_data["id"],callback_data_time, lvl_loc))
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)



@dp.callback_query_handler(dat_mob_loc_ex_retry.filter(action=['figth_mob']))
async def inline_kb_mob_loc_exp_fight2(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            await query.bot.edit_message_text(text=await mob_figth(callback_data["lvl_mob"], int(callback_data["id"]), 'loc'),
                                              message_id=query.message.message_id,
                                              chat_id=query.message.chat.id,
                                              reply_markup=await create_cb_mob_loc_exp_fight(callback_data["id"],callback_data_time, callback_data["lvl_mob"]))
            await query.answer(cache_time=3)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)