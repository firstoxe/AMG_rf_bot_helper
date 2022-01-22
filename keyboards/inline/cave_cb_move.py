from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime
from .cave_cb import upd_cave_btn, upd_cave_btn_all, create_cb_cave

dat_cave_move = CallbackData('caves_move', 'action','id','date')

async def create_cb_cave_move(id, date):
    kb = InlineKeyboardMarkup(row_width=1)
    kb_update = InlineKeyboardButton('🏅 Показать свою лигу', callback_data=dat_cave_move.new('update_cave_lvl_move',str(id),str(date).replace(':',';')))
    view_change = InlineKeyboardButton('🥇🥈🥉 Показать всех', callback_data=dat_cave_move.new('update_cave_any_move',str(id),str(date).replace(':',';')))
    kb.add(kb_update)
    kb.add(view_change)
    return kb


@dp.callback_query_handler(dat_cave_move.filter(action=['update_cave_lvl_move', 'update_cave_any_move']))
async def inline_kb_update_cave__move_callback_handler(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                if callback_data["action"] == 'update_cave_lvl_move':
                    anw_txt = await upd_cave_btn(int(callback_data["id"]))
                    await query.bot.edit_message_text(text=anw_txt,
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_cave(callback_data["id"],callback_data_time,1))
                elif callback_data["action"] == 'update_cave_any_move':
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
