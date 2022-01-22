from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record

from handlers.commands.mob_fight_all import mob_exp_top
from keyboards.inline.mob.mob_loc import create_cb_mob_loc_exp, create_cb_mob_loc_aden
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime


dat_mob_type = CallbackData('mob_type', 'action', 'id', 'date')

async def create_cb_mob_type(id, date):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton('🍀 Обычные мобы', callback_data=dat_mob_type.new('exp',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('🏔 Этер', callback_data=dat_mob_type.new('aden',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('🔮 Топ мобов по опыту', callback_data=dat_mob_type.new('exp_top_5',str(id),str(date).replace(':',';'))))
    return kb


@dp.callback_query_handler(dat_mob_type.filter(action=['exp', 'aden']))
async def inline_kb_update_mob_type(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                if callback_data["action"] == 'exp':
                    await query.bot.edit_message_text(text='Отлично, теперь выбери интересующий тебя диапазон уровней',
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_mob_loc_exp(callback_data["id"],callback_data_time))
                elif callback_data["action"] == 'aden':
                    await query.bot.edit_message_text(text='Отлично, теперь выбери интересующго тебя голема',
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_mob_loc_aden(callback_data["id"],callback_data_time))
            except:
                pass
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)


@dp.callback_query_handler(dat_mob_type.filter(action=['exp_top_5']))
async def inline_kb_update_mob_type_top_exp(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            await query.bot.edit_message_text(text=await mob_exp_top(int(callback_data["id"])),
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_mob_type(callback_data["id"],callback_data_time))
            await query.answer(emojize('Обновлено'), cache_time=5)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)