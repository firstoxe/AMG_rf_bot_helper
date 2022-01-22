from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from asyncpg import Connection, Record
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData


dat = CallbackData('user_conf_notify_', 'action','id','item')


async def create_cb_user(id):
    kb = InlineKeyboardMarkup(row_width=3)
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.notify where id_user=$1''', id,)
    if res[7]:
        kb_dounge = InlineKeyboardButton(emojize(':performing_arts:Данжи:check_mark_button:'),
                                      callback_data=dat.new('dounge',str(id),'7'))
    else:
        kb_dounge = InlineKeyboardButton(emojize(':performing_arts:Данжи:cross_mark:'),
                                      callback_data=dat.new('dounge',str(id),'7'))
    if res[9]:
        kb_caves = InlineKeyboardButton(emojize(':performing_arts:Пещеры:check_mark_button:'),
                                         callback_data=dat.new('caves',str(id),'9'))
    else:
        kb_caves = InlineKeyboardButton(emojize(':performing_arts:Пещеры:cross_mark:'),
                                         callback_data=dat.new('caves',str(id),'9'))
    if res[8]:
        kb_dounge_guild = InlineKeyboardButton(emojize(':performing_arts:Только ГИ:check_mark_button:'),
                                         callback_data=dat.new('dounge_guild',str(id),'8'))
    else:
        kb_dounge_guild = InlineKeyboardButton(emojize(':performing_arts:Только ГИ:cross_mark:'),
                                         callback_data=dat.new('dounge_guild',str(id),'8'))
    if res[1]:
        kb_cw1 = InlineKeyboardButton(emojize(':dagger:ЧВ утро:check_mark_button:'),
                                       callback_data=dat.new('cw1',str(id),'1'))
    else:
        kb_cw1 = InlineKeyboardButton(emojize(':dagger:ЧВ утро:cross_mark:'),
                                       callback_data=dat.new('cw1',str(id),'1'))



    if res[2]:
        kb_cw2 = InlineKeyboardButton(emojize(':dagger:ЧВ день:check_mark_button:'),
                                         callback_data=dat.new('cw2', str(id),'2'))
    else:
        kb_cw2 = InlineKeyboardButton(emojize(':dagger:ЧВ день:cross_mark:'),
                                         callback_data=dat.new('cw2', str(id),'2'))

    if res[3]:
        kb_cw3 = InlineKeyboardButton(emojize(':dagger:ЧВ вечер:check_mark_button:'),
                                             callback_data=dat.new('cw3', str(id),'3'))
    else:
        kb_cw3 = InlineKeyboardButton(emojize(':dagger:ЧВ вечер:cross_mark:'),
                                             callback_data=dat.new('cw3', str(id),'3'))

    if res[4]:
        kb_arena1 = InlineKeyboardButton(emojize(':oncoming_fist_light_skin_tone:Арена ВТ:check_mark_button:'),
                                      callback_data=dat.new('arena1', str(id),'4'))
    else:
        kb_arena1 = InlineKeyboardButton(emojize(':oncoming_fist_light_skin_tone:Арена ВТ:cross_mark:'),
                                      callback_data=dat.new('arena1', str(id),'4'))

    if res[5]:
        kb_arena2 = InlineKeyboardButton(emojize(':oncoming_fist_light_skin_tone:Арена ЧТ:check_mark_button:'),
                                          callback_data=dat.new('arena2', str(id),'5'))
    else:
        kb_arena2 = InlineKeyboardButton(emojize(':oncoming_fist_light_skin_tone:Арена ЧТ:cross_mark:'),
                                          callback_data=dat.new('arena2', str(id),'5'))

    if res[6]:
        kb_arena3 = InlineKeyboardButton(emojize(':oncoming_fist_light_skin_tone:Арена СБ:check_mark_button:'),
                                         callback_data=dat.new('arena3', str(id),'6'))
    else:
        kb_arena3 = InlineKeyboardButton(emojize(':oncoming_fist_light_skin_tone:Арена СБ:cross_mark:'),
                                         callback_data=dat.new('arena3', str(id),'6'))
    if res[10]:
        kb_cave_update = InlineKeyboardButton(emojize(':mountain_cableway:Вход/Выход из пещер:check_mark_button:'),
                                       callback_data=dat.new('caves_update', str(id),'10'))
    else:
        kb_cave_update = InlineKeyboardButton(emojize(':mountain_cableway:Вход/Выход из пещер:cross_mark:'),
                                       callback_data=dat.new('caves_update', str(id),'10'))




    if res[13]:
        kb_bot_update = InlineKeyboardButton(emojize(':counterclockwise_arrows_button:Обновления бота:check_mark_button:'),
                                             callback_data=dat.new('bot_update',str(id),'13'))
    else:
        kb_bot_update = InlineKeyboardButton(emojize(':counterclockwise_arrows_button:Обновления бота:cross_mark:'),
                                             callback_data=dat.new('bot_update',str(id),'13'))
    if res[11]:
        kb_guard = InlineKeyboardButton(emojize(':T-Rex:Страж:check_mark_button:'),
                                             callback_data=dat.new('guard',str(id),'11'))
    else:
        kb_guard = InlineKeyboardButton(emojize(':T-Rex:Страж:cross_mark:'),
                                             callback_data=dat.new('guard',str(id),'11'))
    if res[12]:
        kb_ping_pm = InlineKeyboardButton(emojize(':classical_building:Пинг не в гш:check_mark_button:'),
                                        callback_data=dat.new('ping_pm',str(id),'12'))
    else:
        kb_ping_pm = InlineKeyboardButton(emojize(':classical_building:Пинг не в гш:cross_mark:'),
                                        callback_data=dat.new('ping_pm',str(id),'12'))

    kb.add(kb_caves,kb_dounge,kb_dounge_guild)
    kb.add(kb_arena1,kb_arena2,kb_arena3)
    kb.add(kb_cw1,kb_cw2,kb_cw3)
    kb.add(kb_cave_update)
    kb.add(kb_bot_update)
    kb.add(kb_guard,kb_ping_pm)

    return kb



@dp.callback_query_handler(dat.filter(action=['dounge', 'caves', 'dounge_guild', 'cw1', 'cw2', 'cw3', 'arena1', 'arena2', 'arena3', 'caves_update', 'guard', 'bot_update', 'ping_pm']))
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        pool: Connection = db
        res: Record = await pool.fetchrow('''SELECT * from test.public.notify where id_user=$1''', query.from_user.id,)
        if res[int(callback_data["item"])]:
            arg = False, query.from_user.id
            await pool.fetchrow(f'''UPDATE test.public.notify SET {callback_data["action"]}= $1 where id_user=$2''', *arg)
            await query.answer(emojize(':cross_mark:Отключено!'))
        else:
            arg = True, query.from_user.id
            await pool.fetchrow(f'''UPDATE test.public.notify SET {callback_data["action"]}= $1 where id_user=$2''', *arg)
            await query.answer(emojize(':check_mark_button:Включено!'))
        await query.message.edit_reply_markup(await create_cb_user(query.from_user.id))
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки! Цыц'))