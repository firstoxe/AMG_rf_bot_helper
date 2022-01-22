from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime


dat_help_menu = CallbackData('help_menu', 'action', 'id')

async def create_cb_cave(id):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(InlineKeyboardButton('❗️Тригерры', callback_data=dat_help_menu.new('triggers',str(id))),
           InlineKeyboardButton('🎪 Аукцион', callback_data=dat_help_menu.new('auction',str(id))),
           InlineKeyboardButton('📜 Рецепты', callback_data=dat_help_menu.new('scroll',str(id))))
    kb.add(InlineKeyboardButton('👹 Симулятор', callback_data=dat_help_menu.new('mob_simulation',str(id))),
           InlineKeyboardButton('🚠 Пещеры', callback_data=dat_help_menu.new('caves',str(id))),
           InlineKeyboardButton('🗿 Тотемы', callback_data=dat_help_menu.new('totems',str(id))))
    #kb.add(InlineKeyboardButton('🔙 Назад', callback_data=dat_help_menu.new('Back1',str(id),str(date).replace(':',';'))))

    return kb




@dp.callback_query_handler(dat_help_menu.filter(action=['update_cave_lvl', 'update_cave_any']))
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