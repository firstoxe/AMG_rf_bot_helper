from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime

from states import privacySet


async def anws_generate(query: types.CallbackQuery):
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', query.message.chat.id,)
    anws = (f'Настройки для чата <b>{query.message.chat.title}</b>\n'
            f'id: <code>{query.message.chat.id}</code>\n'
            f'тип: <b>{"group" if query.message.chat.type == types.ChatType.GROUP else types.ChatType.SUPER_GROUP}</b>')
    anws = f'{anws}\n\nОграничение по уровню - '+(f'✅<b>включено</b> 🏅ур. {res["min_lvl"]}-{res["max_lvl"]}' if res["lvl"] else '❌<b>отключено</b>')
    anws = f'{anws}\n\nВход не игрокам рф - {f"❌<b>запрещён</b>" if res["rf_member"] else f"✅<b>разрешён</b>"}'
    anws = f'{anws}\n\nОграничения на вход расам - '+(f'✅<b>включено</b>' if res["race"] else '❌<b>отключено</b>')
    if res["race"]:
        anws = f'{anws}\n✅Вход разрешён - ' + ('‍👩‍🚀' if res['race_bel'] else '') + ('‍🧝‍♀' if res['race_cor'] else '') + ('‍🤖' if res['race_acr'] else '')
        anws = f'{anws}\n❌Вход запрещён' + (' ‍👩‍🚀 ' if not res['race_bel'] else '') + ('‍ 🧝‍♀ ' if not res['race_cor'] else '') + ('‍ 🤖 ' if not res['race_acr'] else '')
    anws = f'{anws}\n\nОграничение по гильдиям - '+(f'✅<b>включено</b>' if res["accept_guild"] else '❌<b>отключено</b>')
    anws = f'{anws}\n\nАвтокик при смене расы - '+(f'✅<b>включено</b>' if res["k_race_change"] else '❌<b>отключено</b>')
    anws = f'{anws}\n\nАвтокик при достижении уровня - '+(f'✅<b>включено</b>' if res["k_lvl_up"] else '❌<b>отключено</b>')
    return anws


async def race_anws_gen(query: types.CallbackQuery):
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', query.message.chat.id,)
    anws = (f'Настройки для чата <b>{query.message.chat.title}</b>\n'
            f'id: <code>{query.message.chat.id}</code>\n'
            f'тип: <b>{"group" if query.message.chat.type == types.ChatType.GROUP else types.ChatType.SUPER_GROUP}</b>')
    anws = f'{anws}\n\nОграничения на вход расам - '+(f'✅<b>включено</b>' if res["race"] else '❌<b>отключено</b>')
    if res["race"]:
        anws = f'{anws}\n\n✅Вход разрешён - ' + ('‍👩‍🚀' if res['race_bel'] else '') + ('‍🧝‍♀' if res['race_cor'] else '') + ('‍🤖' if res['race_acr'] else '')
        anws = f'{anws}\n\n❌Вход запрещён' + (' ‍👩‍🚀 ' if not res['race_bel'] else '') + ('‍ 🧝‍♀ ' if not res['race_cor'] else '') + ('‍ 🤖 ' if not res['race_acr'] else '')
    return anws


async def lvl_anws_gen(query: types.CallbackQuery):
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', query.message.chat.id,)
    anws = (f'Настройки для чата <b>{query.message.chat.title}</b>\n'
            f'id: <code>{query.message.chat.id}</code>\n'
            f'тип: <b>{"group" if query.message.chat.type == types.ChatType.GROUP else types.ChatType.SUPER_GROUP}</b>')
    anws = f'{anws}\n\nОграничения на вход по уровню - '+(f'✅<b>включено</b>' if res["lvl"] else '❌<b>отключено</b>')
    if res["lvl"]:
        anws = f'{anws}\nМинимальный - {res["min_lvl"]}'
        anws = f'{anws}\nМаксимальный - {res["max_lvl"]}'
    return anws


async def lvlup_anws_gen(query: types.CallbackQuery):
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', query.message.chat.id,)
    anws = (f'Настройки для чата <b>{query.message.chat.title}</b>\n'
            f'id: <code>{query.message.chat.id}</code>\n'
            f'тип: <b>{"group" if query.message.chat.type == types.ChatType.GROUP else types.ChatType.SUPER_GROUP}</b>')
    anws = f'{anws}\n\nИсключение из чата по достижению уровня - '+(f'✅<b>включено</b>' if res["k_lvl_up"] else '❌<b>отключено</b>')
    if res["k_lvl_up"]:
        anws = f'{anws}\nМакс лвл для чата- {res["k_lvl_up_data"]}'
    return anws

dat_privacy = CallbackData('privacy', 'action', 'id', 'date')


async def privacy_cb_create(id, chat_id, date):
    kb = InlineKeyboardMarkup(row_width=3)
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', chat_id,)
    kb.add(InlineKeyboardButton('Уровень' + ('✅' if res['lvl'] else '❌'), callback_data=dat_privacy.new('lvl_change',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('Расы'+ ('✅' if res['race'] else '❌'), callback_data=dat_privacy.new('race',str(id),str(date).replace(':',';'))),
           InlineKeyboardButton('Игрок РФ' + ('✅' if res['rf_member'] else '❌'), callback_data=dat_privacy.new('rf_member',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('Кик при повышения уровня' + ('✅' if res['k_lvl_up'] else '❌'), callback_data=dat_privacy.new('lvl_up',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('Кик при смене расы'+ ('✅' if res['k_race_change'] else '❌'), callback_data=dat_privacy.new('race_change',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('Ограничить гильдии'+ ('✅' if res['accept_guild'] else '❌'), callback_data=dat_privacy.new('g_restrict',str(id),str(date).replace(':',';'))))
    return kb

dat_privacy_lvl = CallbackData('privacy_lvl', 'action', 'id', 'date')


async def privacy_cb_create_lvl(id, chat_id, date):
    kb = InlineKeyboardMarkup(row_width=3)
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', chat_id,)
    if res['lvl']:
        kb.add(InlineKeyboardButton('Мин. ур.', callback_data=dat_privacy_lvl.new('min_lvl',str(id),str(date).replace(':',';'))),
               InlineKeyboardButton('Макс. ур.', callback_data=dat_privacy_lvl.new('max_lvl',str(id),str(date).replace(':',';'))))
        kb.add(InlineKeyboardButton('❌Отключить', callback_data=dat_privacy_lvl.new('lvl_on_off',str(id),str(date).replace(':',';'))))
    else:
        kb.add(InlineKeyboardButton('✅Включить', callback_data=dat_privacy_lvl.new('lvl_on_off',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('🔙Главное меню', callback_data=dat_privacy_lvl.new('back_to_main',str(id),str(date).replace(':',';'))))
    return kb

dat_privacy_race = CallbackData('privacy_race', 'action', 'id', 'date')


async def privacy_cb_create_race(id, chat_id, date):
    kb = InlineKeyboardMarkup(row_width=3)
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', chat_id,)
    if res['race']:
        kb.add(InlineKeyboardButton('👩‍🚀Basilaris' + ('✅' if res['race_bel'] else '❌'), callback_data=dat_privacy_race.new('race_bel',str(id),str(date).replace(':',';'))),
               InlineKeyboardButton('🧝‍♀Castitas' + ('✅' if res['race_cor'] else '❌'), callback_data=dat_privacy_race.new('race_cor',str(id),str(date).replace(':',';'))),
               InlineKeyboardButton('🤖Aquilla' + ('✅' if res['race_acr'] else '❌'), callback_data=dat_privacy_race.new('race_acr',str(id),str(date).replace(':',';'))))
        kb.add(InlineKeyboardButton('❌Отключить', callback_data=dat_privacy_race.new('race_on_off',str(id),str(date).replace(':',';'))))
    else:
        kb.add(InlineKeyboardButton('✅Включить', callback_data=dat_privacy_race.new('race_on_off',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('🔙Главное меню', callback_data=dat_privacy_race.new('back_to_main',str(id),str(date).replace(':',';'))))
    return kb


dat_privacy_lvlup = CallbackData('privacy_lvlup', 'action', 'id', 'date')


async def privacy_cb_create_lvlup(id, chat_id, date):
    kb = InlineKeyboardMarkup(row_width=3)
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', chat_id,)
    if res['k_lvl_up']:
        kb.add(InlineKeyboardButton('Задать уровнеь', callback_data=dat_privacy_lvlup.new('set_lvl_kick',str(id),str(date).replace(':',';'))))
        kb.add(InlineKeyboardButton('❌Отключить', callback_data=dat_privacy_lvlup.new('lvlup_on_off',str(id),str(date).replace(':',';'))))
    else:
        kb.add(InlineKeyboardButton('✅Включить', callback_data=dat_privacy_lvlup.new('lvlup_on_off',str(id),str(date).replace(':',';'))))
    kb.add(InlineKeyboardButton('🔙Главное меню', callback_data=dat_privacy_lvlup.new('back_to_main',str(id),str(date).replace(':',';'))))
    return kb


@dp.callback_query_handler(dat_privacy_lvlup.filter(action=['back_to_main']))
@dp.callback_query_handler(dat_privacy_lvl.filter(action=['back_to_main']))
@dp.callback_query_handler(dat_privacy_race.filter(action=['back_to_main']))
async def inline_kb_privacy_back_main(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                await query.answer(cache_time=1)
                await query.message.edit_text(text=await anws_generate(query), reply_markup=await privacy_cb_create(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
            except:
                await query.answer(cache_time=1)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=60)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /privacy для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=60)


@dp.callback_query_handler(dat_privacy.filter(action=['rf_member']))
async def inline_kb_privacy_member_rf(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                pool: Connection = db
                if await pool.fetchval('''SELECT rf_member from test.public.chats where id_chat=$1''', query.message.chat.id,):
                    arg = False, query.message.chat.id
                    await pool.fetchrow('''UPDATE test.public.chats SET rf_member=$1 where id_chat=$2''', *arg)
                else:
                    arg = True, query.message.chat.id
                    await pool.fetchrow('''UPDATE test.public.chats SET rf_member=$1 where id_chat=$2''', *arg)
                await query.answer(cache_time=1)

                await query.message.edit_text(text=await anws_generate(query), reply_markup=await privacy_cb_create(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
            except:
                await query.answer(cache_time=1)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=60)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /privacy для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=60)


@dp.callback_query_handler(dat_privacy.filter(action=['race_change']))
async def inline_kb_privacy_race_change(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                pool: Connection = db
                if await pool.fetchval('''SELECT k_race_change from test.public.chats where id_chat=$1''', query.message.chat.id,):
                    arg = False, query.message.chat.id
                    await pool.fetchrow('''UPDATE test.public.chats SET k_race_change=$1 where id_chat=$2''', *arg)
                else:
                    arg = True, query.message.chat.id
                    await pool.fetchrow('''UPDATE test.public.chats SET k_race_change=$1 where id_chat=$2''', *arg)
                await query.answer(cache_time=1)
                await query.message.edit_text(text=await anws_generate(query), reply_markup=await privacy_cb_create(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
            except:
                await query.answer(cache_time=1)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=60)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /privacy для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=60)


@dp.callback_query_handler(dat_privacy.filter(action=['race', 'lvl_change', 'lvl_up']))
async def inline_kb_privacy_race_change(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                await query.answer(cache_time=1)
                if callback_data["action"] == 'race':
                    await query.message.edit_text(text=await race_anws_gen(query), reply_markup=await privacy_cb_create_race(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
                elif callback_data["action"] == 'lvl_change':
                    await query.message.edit_text(text=await lvl_anws_gen(query), reply_markup=await privacy_cb_create_lvl(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
                elif callback_data["action"] == 'lvl_up':
                    await query.message.edit_text(text=await lvlup_anws_gen(query), reply_markup=await privacy_cb_create_lvlup(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
            except Exception as e:
                await query.answer(cache_time=1)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=60)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /privacy для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=60)


@dp.callback_query_handler(dat_privacy_race.filter(action=['race_bel','race_cor','race_acr','race_on_off']))
async def inline_kb_privacy_race_change(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                pool: Connection = db
                if callback_data["action"] == 'race_on_off':
                    if await pool.fetchval('''SELECT race from test.public.chats where id_chat=$1''', query.message.chat.id,):
                        arg = False, query.message.chat.id
                        await pool.fetchrow('''UPDATE test.public.chats SET race=$1 where id_chat=$2''', *arg)
                    else:
                        arg = True, query.message.chat.id
                        await pool.fetchrow('''UPDATE test.public.chats SET race=$1 where id_chat=$2''', *arg)
                    await query.message.edit_text(text=await race_anws_gen(query), reply_markup=await privacy_cb_create_race(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
                else:
                    if await pool.fetchval(f'''SELECT {callback_data["action"]} from test.public.chats where id_chat=$1''', query.message.chat.id,):
                        arg = False, query.message.chat.id
                        await pool.fetchrow(f'''UPDATE test.public.chats SET {callback_data["action"]}=$1 where id_chat=$2''', *arg)
                    else:
                        arg = True, query.message.chat.id
                        await pool.fetchrow(f'''UPDATE test.public.chats SET {callback_data["action"]}=$1 where id_chat=$2''', *arg)
                    await query.answer(cache_time=1)
                await query.message.edit_text(text=await race_anws_gen(query), reply_markup=await privacy_cb_create_race(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
            except:
                await query.answer(cache_time=1)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=60)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /privacy для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=60)


@dp.callback_query_handler(dat_privacy_lvl.filter(action=['min_lvl','max_lvl','lvl_on_off']))
async def inline_kb_privacy_set_lvl(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                pool: Connection = db
                if callback_data["action"] == 'lvl_on_off':
                    if await pool.fetchval('''SELECT lvl from test.public.chats where id_chat=$1''', query.message.chat.id,):
                        arg = False, query.message.chat.id
                        await pool.fetchrow('''UPDATE test.public.chats SET lvl=$1 where id_chat=$2''', *arg)
                    else:
                        arg = True, query.message.chat.id
                        await pool.fetchrow('''UPDATE test.public.chats SET lvl=$1 where id_chat=$2''', *arg)
                    await query.message.edit_text(text=await lvl_anws_gen(query), reply_markup=await privacy_cb_create_lvl(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
                elif callback_data["action"] == 'min_lvl':
                    anws_msg_id = await query.message.answer('Укажи минимальный уровень:\nДля отмены напиши "нет"')
                    await privacySet.wait_add_min_lvl.set()
                    await state.update_data(anws_msg_id=anws_msg_id.message_id)
                    await state.update_data(inlin_kb_id=query.message.message_id)
                    await state.update_data(id=int(callback_data["id"]))
                    await state.update_data(date=callback_data["date"])
                    await state.update_data(chat_id=query.message.chat.id)
                elif callback_data["action"] == 'max_lvl':
                    anws_msg_id = await query.message.answer('Укажи максимальный уровень:\nДля отмены напиши "нет"')
                    await privacySet.wait_add_max_lvl.set()
                    await state.update_data(anws_msg_id=anws_msg_id.message_id)
                    await state.update_data(inlin_kb_id=query.message.message_id)
                    await state.update_data(id=int(callback_data["id"]))
                    await state.update_data(date=callback_data["date"])
                    await state.update_data(chat_id=query.message.chat.id)
                await query.answer(cache_time=1)
            except:
                await query.answer(cache_time=1)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=60)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /privacy для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=60)


@dp.callback_query_handler(dat_privacy_lvlup.filter(action=['set_lvl_kick', 'lvlup_on_off']))
async def inline_kb_privacy_set_lvlup(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            try:
                pool: Connection = db
                if callback_data["action"] == 'lvlup_on_off':
                    if await pool.fetchval('''SELECT k_lvl_up from test.public.chats where id_chat=$1''', query.message.chat.id,):
                        arg = False, query.message.chat.id
                        await pool.fetchrow('''UPDATE test.public.chats SET k_lvl_up=$1 where id_chat=$2''', *arg)
                    else:
                        arg = True, query.message.chat.id
                        await pool.fetchrow('''UPDATE test.public.chats SET k_lvl_up=$1 where id_chat=$2''', *arg)
                    await query.message.edit_text(text=await lvlup_anws_gen(query), reply_markup=await privacy_cb_create_lvlup(int(callback_data["id"]),query.message.chat.id,callback_data["date"]))
                elif callback_data["action"] == 'set_lvl_kick':
                    anws_msg_id = await query.message.answer('Укажи максимальный уровень для чата:\nДля отмены напиши "нет"')
                    await privacySet.wait_add_lvl_up.set()
                    await state.update_data(anws_msg_id=anws_msg_id.message_id)
                    await state.update_data(inlin_kb_id=query.message.message_id)
                    await state.update_data(id=int(callback_data["id"]))
                    await state.update_data(date=callback_data["date"])
                    await state.update_data(chat_id=query.message.chat.id)
                await query.answer(cache_time=1)
            except:
                await query.answer(cache_time=1)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=60)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /privacy для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=60)