import re

from aiogram import types
from loader import dp, db
from aiogram.utils.text_decorations import html_decoration
from aiogram.utils.emoji import demojize,emojize
from data.config import admins
from re import sub
from asyncpg import Record, Connection
from filters.guild_check import check_g
from utils.misc import rate_limit
from handlers.commands.recipe.item import stat_for_item


@rate_limit(0, 'convert_return')
@dp.message_handler(content_types=['text'], text_contains=['/a_return_'])
async def bot_echo(message: types.Message):
    aws = sub(r'/a_buy_\w{,9}', r'<a href="http://t.me/share/url?url=\g<0>">\g<0></a>', message.text.replace('/a_return_', '/a_buy_'))
    pool: Connection = db
    user_nick: Record = await pool.fetchrow('''SELECT guild,nickname FROM test.public."user" 
                                                WHERE id = $1''', message.from_user.id,)
    if message.text.find('Список выставленных предметов на аукцион. Чтобы вернуть предмет, кликни на команду напротив нужного лота.')!= -1:
        aws = aws.replace('Список выставленных предметов на аукцион. Чтобы вернуть предмет, кликни на команду напротив нужного лота.', f'Список предметов от {check_g(user_nick["guild"])}<a href="tg://user?id={message.from_user.id}">{emojize(user_nick["nickname"])}</a>:')+'\n\n<b>Команды кликабельны</b>'
    await message.reply(aws)
    await message.delete()


@rate_limit(0, 'convert_buy')
@dp.message_handler(content_types=types.ContentTypes.TEXT, text_contains=['/a_buy_'])
async def bot_echo(message: types.Message):
    aws = sub(r'/a_buy_\w{,9}', r'<a href="http://t.me/share/url?url=\g<0>">\g<0></a>', message.text)
    pool: Connection = db
    user_nick: Record = await pool.fetchrow('''SELECT guild,nickname FROM test.public."user" 
                                                WHERE id = $1''', message.from_user.id,)
    if message.text.find('Список выставленных предметов на аукцион. Чтобы вернуть предмет, кликни на команду напротив нужного лота.')!= -1:
        aws = aws.replace('Список выставленных предметов на аукцион. Чтобы вернуть предмет, кликни на команду напротив нужного лота.', f'Список предметов от {check_g(user_nick["guild"])}<a href="tg://user?id={message.from_user.id}">{emojize(user_nick["nickname"])}</a>:')+'\n\n<b>Команды кликабельны</b>'
    await message.reply(aws)
    await message.delete()


@rate_limit(2, 'trigger')
@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPER_GROUP], content_types=types.ContentTypes.TEXT, is_trigger=True)
async def bot_trigger_echo(message: types.Message):
    pool: Connection = db
    arg = message.chat.id, message.text
    trig: Record = await pool.fetchrow('''SELECT * from test.public.triggers_chat where id_chat= $1 and tg_name = $2''', *arg)
    if trig["tg_type"] == 'текст':
        await message.answer(trig["tg_text"])
    elif trig["tg_type"] == 'гифка':
        await message.answer_animation(animation=trig["tg_animation"])
    elif trig["tg_type"] == 'фото':
        await message.answer_photo(photo=trig["tg_photo"], caption=trig["tg_text"])
    elif trig["tg_type"] == 'аудио':
        await message.answer_audio(audio=trig["tg_audio"], caption=trig["tg_text"])
    elif trig["tg_type"] == 'стикер':
        await message.answer_sticker(sticker=trig["tg_sticker"])
    elif trig["tg_type"] == 'видео':
        await message.answer_video(video=trig["tg_video"], caption=trig["tg_text"])


@rate_limit(1, 'echo_item')
@dp.message_handler(content_types=types.ContentTypes.TEXT, is_echo_item=True)
async def bot_trigger_echo_item(message: types.Message):
    pool: Connection = db
    list_item = []
    rec = re.compile(r'\b\w+\s\b\w+')
    for item in demojize(message.text).splitlines():
        try:
            if rec.findall(item):
                record: Record = await pool.fetchrow('SELECT * FROM test.public.recipes '
                                                     'where name=$1 or name_a = $1 or name_b = $1', rec.findall(item)[0].lower())
                item_stat = item.split(' ')
                if item_stat[0].find(')') != -1:
                    item_stat.remove(item_stat[0])
                list_item.append(f'{await stat_for_item(item_stat,record,record["name"])}\n')
        except Exception as rr:
            pass
    await message.answer('\n'.join(list_item))



@rate_limit(0, 'echo_shiff_chat_user')
@dp.message_handler(content_types=types.ContentTypes.TEXT, chat_type=[types.ChatType.GROUP,types.ChatType.SUPER_GROUP])
async def bot_new_all_chats_member(message: types.Message):

    pool: Connection = db
    chat_find: Record = await pool.fetchval('''SELECT id_chat from test.public.chats where id_chat= $1''',
                                                message.chat.id, )
    if not chat_find:
        arg = message.chat.id, message.chat.title, message.chat.type, True
        await pool.fetchval('''INSERT INTO test.public.chats VALUES ($1,$2,$3,$4 )''', *arg)
    if not message.from_user.is_bot:
        arg = message.chat.id, message.from_user.id
        memb: Record = await pool.fetchrow('''SELECT * from test.public.members_in_chats where id_chat= $1 and id=$2''', *arg)
        if memb:
            arg = message.chat.id, message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, (await message.bot.get_chat_member(message.chat.id,message.from_user.id))["status"]
            await pool.fetchval('''UPDATE test.public.members_in_chats SET username=$3, firstname=$4, lastname=$5, status=$6  where id_chat= $1 and id=$2''',
                    *arg)
        else:
            arg = message.chat.id, message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, (await message.bot.get_chat_member(message.chat.id,message.from_user.id))["status"]
            await pool.fetchval('''INSERT INTO test.public.members_in_chats VALUES ($1,$2,$3,$4,$5,$6)''', *arg)


