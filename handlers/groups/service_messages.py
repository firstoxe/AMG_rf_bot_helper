from aiogram import types
from loader import dp, db
from aiogram.utils.text_decorations import html_decoration
from data.config import admins
from re import sub
from asyncpg import Record, Connection
from aiogram.utils.emoji import emojize
from filters.work_with_user import helper_user
from utils.misc import rate_limit


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def bot_new_all_chats_member(message: types.Message):
    pool: Connection = db
    chat_find: Record = await pool.fetchval('''SELECT id_chat from test.public.chats where id_chat= $1''',
                                            message.chat.id, )
    if not chat_find:
        arg = message.chat.id, message.chat.title, message.chat.type, True
        await pool.fetchval('''INSERT INTO test.public.chats VALUES ($1,$2,$3,$4 )''', *arg)
    for item in message.new_chat_members:
        if not item.is_bot:
            arg = message.chat.id, item.id
            memb: Record = await pool.fetchrow(
                '''SELECT * from test.public.members_in_chats where id_chat= $1 and id=$2''', *arg)
            if memb:

                arg = message.chat.id, item.id, item.username, item.first_name, item.last_name, 'member'
                await pool.fetchval(
                    '''UPDATE test.public.members_in_chats SET username=$3, firstname=$4, lastname=$5, status=$6  where id_chat= $1 and id=$2''',
                    *arg)
                await message.answer(f'{await helper_user(item.id)} с возвращением!')
            else:
                arg = message.chat.id, item.id, item.first_name, item.last_name, item.username, 'member'
                await pool.fetchval('''INSERT INTO test.public.members_in_chats VALUES ($1,$2,$3,$4,$5,$6)''', *arg)
                await message.answer(f'{await helper_user(item.id)} ну, допустим, привет!')


@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def bot_left_all_chats_member(message: types.Message):
    pool: Connection = db
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f'{await helper_user(message.left_chat_member.id)} покинул нас!')
    elif message.from_user.id == 1392814993:
        return
    else:
        await message.answer(f'{await helper_user(message.left_chat_member.id)} кикнут из чата '
                             f'пользователем {message.from_user.get_mention(as_html=True)}')

    chat_find: Record = await pool.fetchval('''SELECT id_chat from test.public.chats where id_chat= $1''',
                                            message.chat.id, )
    if not chat_find:
        arg = message.chat.id, message.chat.title, message.chat.type, True
        await pool.fetchval('''INSERT INTO test.public.chats VALUES ($1,$2,$3,$4 )''', *arg)
    arg = message.chat.id, message.left_chat_member.id
    memb: Record = await pool.fetchrow('''SELECT * from test.public.members_in_chats where id_chat= $1 and id=$2''',
                                       *arg)
    if not message.left_chat_member.is_bot:
        if memb:
            arg = message.chat.id, message.left_chat_member.id, message.left_chat_member.username, message.left_chat_member.first_name, message.left_chat_member.last_name, 'left'
            await pool.fetchval(
                '''UPDATE test.public.members_in_chats SET username=$3, firstname=$4, lastname=$5, status=$6  where id_chat= $1 and id=$2''',
                *arg)
        else:
            arg = message.chat.id, message.left_chat_member.id, message.left_chat_member.first_name, message.left_chat_member.last_name, message.left_chat_member.username, 'left'
            await pool.fetchval('''INSERT INTO test.public.members_in_chats VALUES ($1,$2,$3,$4,$5,$6)''', *arg)


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_TITLE)
async def bot_new_chat_title(message: types.Message):
    pool: Connection = db
    chat_find: Record = await pool.fetchval('''SELECT id_chat from test.public.chats where id_chat= $1''',
                                            message.chat.id, )
    if not chat_find:
        arg = message.chat.id, message.new_chat_title, message.chat.type, True
        await pool.fetchval('''INSERT INTO test.public.chats VALUES ($1,$2,$3,$4 )''', *arg)
    elif chat_find:
        arg = message.chat.id, message.new_chat_title
        await pool.fetchval('''UPDATE test.public.chats SET name_chat=$2 WHERE id_chat=$1''', *arg)


@dp.message_handler(content_types=types.ContentTypes.MIGRATE_TO_CHAT_ID)
async def bot_new_chat_title(message: types.Message):
    pool: Connection = db
    chat_find: Record = await pool.fetchval('''SELECT id_chat from test.public.chats where id_chat= $1''',
                                            message.chat.id, )
    if not chat_find:
        arg = message.migrate_to_chat_id, message.chat.title, message.chat.type, True
        await pool.fetchval('''INSERT INTO test.public.chats VALUES ($1,$2,$3,$4 )''', *arg)
    elif chat_find:
        arg = message.chat.id, message.migrate_to_chat_id
        await pool.fetchval('''UPDATE test.public.chats SET id_chat=$2 WHERE id_chat=$1''', *arg)
        await pool.fetchval('''UPDATE test.public.members_in_chats SET id_chat=$2 WHERE id_chat=$1''', *arg)


@dp.message_handler(content_types=types.ContentTypes.MIGRATE_FROM_CHAT_ID)
async def bot_new_chat_title(message: types.Message):
    pool: Connection = db
    chat_find: Record = await pool.fetchval('''SELECT id_chat from test.public.chats where id_chat= $1''',
                                            message.chat.id,)
    if not chat_find:
        arg = message.migrate_from_chat_id, message.chat.title, message.chat.type, True
        await pool.fetchval('''INSERT INTO test.public.chats VALUES ($1,$2,$3,$4 )''', *arg)
    elif chat_find:
        arg = message.chat.id, message.migrate_from_chat_id
        await pool.fetchval('''UPDATE test.public.chats SET id_chat=$2 WHERE id_chat=$1''', *arg)
        await pool.fetchval('''UPDATE test.public.members_in_chats SET id_chat=$2 WHERE id_chat=$1''', *arg)