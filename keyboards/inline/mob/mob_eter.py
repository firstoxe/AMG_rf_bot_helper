from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record

from handlers.commands.mob_fight_all import mob_figth
from keyboards.inline.mob.mob_loc import create_cb_mob_loc_aden
from keyboards.inline.mob.mob_type import create_cb_mob_type
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime


dat_mob_loc_etir = CallbackData('mob_eter', 'action', 'id', 'date', 'mob')

async def create_cb_mob_loc_etir(id, date, mob):
    kb1 = InlineKeyboardMarkup(row_width=1)
    kb1.add(InlineKeyboardButton('🔄 Обновить', callback_data=dat_mob_loc_etir.new('eter_retry', str(id), str(date).replace(':',';'), str(mob))))
    kb1.add(InlineKeyboardButton('🔙 Назад', callback_data=dat_mob_loc_etir.new('BackEter',str(id),str(date).replace(':',';'), str(mob))))
    return kb1


@dp.callback_query_handler(dat_mob_loc_etir.filter(action=['eter_retry', 'BackEter']))
async def inline_kb_mob_loc_eter_fight2(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            if callback_data["action"] == "eter_retry":
                await query.bot.edit_message_text(text=await mob_figth(callback_data["mob"], int(callback_data["id"]), 'eter'),
                                                  message_id=query.message.message_id,
                                                  chat_id=query.message.chat.id,
                                                  reply_markup=await create_cb_mob_loc_etir(callback_data["id"],callback_data_time, callback_data["mob"]))
                await query.answer(cache_time=3)
            elif callback_data["action"] == 'BackEter':
                await query.bot.edit_message_text(text='Отлично, теперь выбери интересующго тебя голема',
                                                  message_id=query.message.message_id,
                                                  chat_id=query.message.chat.id,
                                                  reply_markup=await create_cb_mob_loc_aden(callback_data["id"],callback_data_time))
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=3)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /mob для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=3)