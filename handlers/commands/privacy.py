import ast

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from asyncpg import Connection, Record
from loader import dp, db
from aiogram.types.chat import ChatType
from keyboards.inline.privacy import privacy_cb_create, privacy_cb_create_lvl, privacy_cb_create_lvlup
from states.privacy_add_guild import privacySet
from utils.misc import rate_limit
from aiogram.utils.emoji import demojize



@rate_limit(3, 'privacy')
@dp.message_handler(commands='privacy', chat_type=[ChatType.GROUP, ChatType.SUPER_GROUP], is_chat_admin=True)
async def bot_command_privacy(message: types.Message):
    pool: Connection = db
    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', message.chat.id,)
    anws = (f'Настройки для чата <b>{message.chat.title}</b>\n'
            f'id: <code>{message.chat.id}</code>\n'
            f'тип: <b>{"group" if message.chat.type == ChatType.GROUP else ChatType.SUPER_GROUP}</b>')
    anws = f'{anws}\n\nОграничение по уровню - '+(f'✅<b>включено</b> 🏅ур. {res["min_lvl"]}-{res["max_lvl"]}' if res["lvl"] else '❌<b>отключено</b>')
    anws = f'{anws}\n\nВход не игрокам рф - {f"❌<b>запрещён</b>" if res["rf_member"] else f"✅<b>разрешён</b>"}'
    anws = f'{anws}\n\nОграничение по расам -' + (f"✅<b>включено</b> {'✅👩‍🚀' if res['race_bel'] else '❌👩‍🚀'} {'✅🧝‍♀' if res['race_cor'] else '❌🧝‍♀'} {'✅🤖' if res['race_acr'] else '❌🤖'}" if res["race"] else f"❌<b>отключено</b>")
    anws = f'{anws}\n\nОграничение по гильдиям - '+(f'✅<b>включено</b>' if res["accept_guild"] else '❌<b>отключено</b>')
    anws = f'{anws}\n\nАвтокик при смене расы - '+(f'✅<b>включено</b>' if res["k_race_change"] else '❌<b>отключено</b>')
    anws = f'{anws}\n\nАвтокик при достижении уровня - '+(f'✅<b>включено</b>' if res["k_lvl_up"] else '❌<b>отключено</b>')
    await message.answer(anws, reply_markup=await privacy_cb_create(message.from_user.id, message.chat.id, message.date))


@dp.message_handler(state=[privacySet.wait_add_guild, privacySet.wait_add_max_lvl,
                           privacySet.wait_add_min_lvl,privacySet.wait_add_lvl_up], text=['нет', 'Нет'])
async def bot_fsm_cancel_add_guild(message: types.Message, state: FSMContext):
    await message.delete()
    await message.bot.delete_message(chat_id=(await state.get_data()).get("chat_id"),message_id=(await state.get_data()).get("anws_msg_id"))
    await state.finish()


@dp.message_handler(state=privacySet.wait_add_guild, content_types=types.ContentTypes.TEXT)
async def bot_fsm_add_guild(message: types.Message, state: FSMContext):
    await state.finish()
    pool: Connection = db
    if await pool.fetchrow('''SELECT guild from test.public."user" where guild=$1 GROUP BY guild''', demojize(message.text),):
        res = await pool.fetchrow('''SELECT accept_guild_data from test.public.chats where id_chat=$1''', message.chat.id,)
        if res:
            res = ast.literal_eval(res)
            if demojize(message.text) in res:
                await message.answer('Нельзя добавить одну гильдию дважды')
                CancelHandler()
        else:
            res = []
        res.append(demojize(message.text))
        arg = str(res), message.chat.id
        if await pool.fetchrow('''UPDATE test.public.chats SET accept_guild_data=$1 where id_chat=$2 RETURNING TRUE''', *arg):
            await message.answer('Гильдия добавлена в белый список!')


@dp.message_handler(state=privacySet.wait_add_min_lvl, content_types=types.ContentTypes.TEXT)
async def bot_fsm_set_min_lvl(message: types.Message, state: FSMContext):
    pool: Connection = db
    if message.text.isdigit():
        pass
        if 0<len(message.text)<3:
            if int(message.text)>0:
                arg = int(message.text), message.chat.id
                if await pool.fetchrow('''UPDATE test.public.chats SET min_lvl=$1 where id_chat=$2 RETURNING TRUE''', *arg):
                    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', message.chat.id,)
                    anws = (f'Настройки для чата <b>{message.chat.title}</b>\n'
                            f'id: <code>{message.chat.id}</code>\n'
                            f'тип: <b>{"group" if message.chat.type == types.ChatType.GROUP else types.ChatType.SUPER_GROUP}</b>')
                    anws = f'{anws}\n\nОграничения на вход по уровню - '+(f'✅<b>включено</b>' if res["lvl"] else '❌<b>отключено</b>')
                    if res["lvl"]:
                        anws = f'{anws}\nМинимальный - {res["min_lvl"]}'
                        anws = f'{anws}\nМаксимальный - {res["max_lvl"]}'
                    await message.bot.edit_message_text(text=anws,chat_id=(await state.get_data()).get("chat_id"),message_id=(await state.get_data()).get("inlin_kb_id"),reply_markup=await privacy_cb_create_lvl((await state.get_data()).get("id"),(await state.get_data()).get("chat_id"),(await state.get_data()).get("date")))
                    await message.delete()
                    await message.bot.delete_message(chat_id=(await state.get_data()).get("chat_id"),message_id=(await state.get_data()).get("anws_msg_id"))
                    await state.finish()


@dp.message_handler(state=privacySet.wait_add_max_lvl, content_types=types.ContentTypes.TEXT)
async def bot_fsm_set_max_lvl(message: types.Message, state: FSMContext):
    pool: Connection = db
    if message.text.isdigit():
        pass
        if 0<len(message.text)<3:
            if int(message.text)>0:
                arg = int(message.text), message.chat.id
                if await pool.fetchrow('''UPDATE test.public.chats SET max_lvl=$1 where id_chat=$2 RETURNING TRUE''', *arg):
                    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', message.chat.id,)
                    anws = (f'Настройки для чата <b>{message.chat.title}</b>\n'
                            f'id: <code>{message.chat.id}</code>\n'
                            f'тип: <b>{"group" if message.chat.type == types.ChatType.GROUP else types.ChatType.SUPER_GROUP}</b>')
                    anws = f'{anws}\n\nОграничения на вход по уровню - '+(f'✅<b>включено</b>' if res["lvl"] else '❌<b>отключено</b>')
                    if res["lvl"]:
                        anws = f'{anws}\nМинимальный - {res["min_lvl"]}'
                        anws = f'{anws}\nМаксимальный - {res["max_lvl"]}'
                    await message.bot.edit_message_text(text=anws,chat_id=(await state.get_data()).get("chat_id"),message_id=(await state.get_data()).get("inlin_kb_id"),reply_markup=await privacy_cb_create_lvl((await state.get_data()).get("id"),(await state.get_data()).get("chat_id"),(await state.get_data()).get("date")))
                    await message.delete()
                    await message.bot.delete_message(chat_id=(await state.get_data()).get("chat_id"),message_id=(await state.get_data()).get("anws_msg_id"))
                    await state.finish()


@dp.message_handler(state=privacySet.wait_add_lvl_up, content_types=types.ContentTypes.TEXT)
async def bot_fsm_set_up_lvl(message: types.Message, state: FSMContext):
    pool: Connection = db
    if message.text.isdigit():
        pass
        if 0<len(message.text)<3:
            if int(message.text)>0:
                arg = int(message.text), message.chat.id
                if await pool.fetchrow('''UPDATE test.public.chats SET k_lvl_up_data=$1 where id_chat=$2 RETURNING TRUE''', *arg):
                    res: Record = await pool.fetchrow('''SELECT * from test.public.chats where id_chat=$1''', message.chat.id,)
                    anws = (f'Настройки для чата <b>{message.chat.title}</b>\n'
                            f'id: <code>{message.chat.id}</code>\n'
                            f'тип: <b>{"group" if message.chat.type == types.ChatType.GROUP else types.ChatType.SUPER_GROUP}</b>')
                    anws = f'{anws}\n\nИсключение из чата по достижению уровня - '+(f'✅<b>включено</b>' if res["k_lvl_up"] else '❌<b>отключено</b>')
                    if res["k_lvl_up"]:
                        anws = f'{anws}\nМакс лвл для чата- {res["k_lvl_up_data"]}'
                    await message.bot.edit_message_text(text=anws,chat_id=(await state.get_data()).get("chat_id"),message_id=(await state.get_data()).get("inlin_kb_id"),reply_markup=await privacy_cb_create_lvlup((await state.get_data()).get("id"),(await state.get_data()).get("chat_id"),(await state.get_data()).get("date")))
                    await message.delete()
                    await message.bot.delete_message(chat_id=(await state.get_data()).get("chat_id"),message_id=(await state.get_data()).get("anws_msg_id"))
                    await state.finish()