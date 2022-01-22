from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record

from handlers.commands.mob_fight_all import mob_figth

from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime


dat_mob_loc = CallbackData('mob_loc', 'action', 'id', 'date')

async def create_cb_mob_loc_exp(id, date):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(InlineKeyboardButton('2-10', callback_data=dat_mob_loc.new('2-10',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('11-20', callback_data=dat_mob_loc.new('11-20',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('21-30', callback_data=dat_mob_loc.new('21-30',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('31-40', callback_data=dat_mob_loc.new('31-40',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('41-50', callback_data=dat_mob_loc.new('41-50',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('51-60', callback_data=dat_mob_loc.new('51-60',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('🔙 Назад', callback_data=dat_mob_loc.new('Back1',str(id),str(date).replace(':',';'))))
    return kb


async def create_cb_mob_loc_aden(id, date):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(InlineKeyboardButton('9', callback_data=dat_mob_loc.new('9',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('19', callback_data=dat_mob_loc.new('19',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('29', callback_data=dat_mob_loc.new('29',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('39', callback_data=dat_mob_loc.new('39',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('49', callback_data=dat_mob_loc.new('49',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('53', callback_data=dat_mob_loc.new('53',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('58', callback_data=dat_mob_loc.new('58',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('🔙 Назад', callback_data=dat_mob_loc.new('Back1',str(id),str(date).replace(':',';'))))
    return kb



@dp.callback_query_handler(dat_mob_loc.filter(action=['9', '19', '29', '39', '49', '53', '58']))
async def inline_kb_mob_loc_eter(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
                lvl_mob = callback_data["action"]
                from keyboards.inline.mob.mob_eter import create_cb_mob_loc_etir
                await query.bot.edit_message_text(text=await mob_figth(lvl_mob, int(callback_data["id"]), 'eter'),
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_mob_loc_etir(callback_data["id"],callback_data_time, lvl_mob))
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)


@dp.callback_query_handler(dat_mob_loc.filter(action=['2-10', '11-20', '21-30', '31-40', '41-50', '51-60']))
async def inline_kb_mob_loc_exp(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            from keyboards.inline.mob.mob_exp import create_cb_mob_loc_exp_lvl
            await query.bot.edit_message_text(text='Выбери уровень моба 👹',
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_mob_loc_exp_lvl(callback_data["id"],callback_data_time, callback_data["action"]))
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)


@dp.callback_query_handler(dat_mob_loc.filter(action=['Back1']))
async def inline_kb_mob_loc_back1(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            from .mob_type import create_cb_mob_type
            await query.bot.edit_message_text(text='Выбери интересущий раздел:',
                                                chat_id=query.message.chat.id,
                                                message_id=query.message.message_id,
                                                reply_markup=await create_cb_mob_type(callback_data["id"],callback_data_time))
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)