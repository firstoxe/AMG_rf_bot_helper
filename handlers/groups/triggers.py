from aiogram import types
from loader import dp, db
from aiogram.utils.text_decorations import html_decoration
from data.config import admins
from asyncpg import Record, Connection
from utils.misc import rate_limit
from aiogram import types



@rate_limit(1, 'add_trigger')
@dp.message_handler(commands='trigger',
                    chat_type=[types.ChatType.GROUP,types.ChatType.SUPER_GROUP],
                    is_reply=True,
                    is_chat_admin=True,
                    commands_prefix='+')
async def bot_trigger_add_or_update(message: types.Message):
    if message.text != '+trigger':
        try:
            pool: Connection = db
            if message.reply_to_message.content_type == 'text':
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow('''SELECT tg_name FROM test.public.triggers_chat WHERE tg_name = $1 and id_chat=$2''', *arg,)
                reply_text = message.reply_to_message.text
                arg = 'текст', name_trigger, reply_text, message.chat.id, message.from_user.id
                if find_tg:
                    if await pool.fetchval('''UPDATE test.public.triggers_chat SET tg_text=$3,user_add=$5, tg_type=$1 WHERE tg_name=$2 and user_add=$5 and id_chat = $4 RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список тригерров /trigger')
                else:
                    if await pool.fetchval('''INSERT INTO test.public.triggers_chat (tg_type, tg_name , tg_text, id_chat, user_add) VALUES ($1,$2,$3,$4,$5) RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список тригерров /trigger')
            if message.reply_to_message.content_type == "animation":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow('''SELECT tg_name FROM test.public.triggers_chat WHERE tg_name = $1 and id_chat=$2''', *arg,)
                reply_anim_id = message.reply_to_message.animation.file_id
                arg = 'гифка', name_trigger, reply_anim_id, message.chat.id, message.from_user.id
                if find_tg:
                    if await pool.fetchval('''UPDATE test.public.triggers_chat SET tg_animation=$3,user_add=$5, tg_type=$1 WHERE tg_name=$2 and user_add=$5 and id_chat = $4 RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список тригерров /trigger')
                else:
                    if await pool.fetchval('''INSERT INTO test.public.triggers_chat (tg_type, tg_name , tg_animation, id_chat, user_add) VALUES ($1,$2,$3,$4,$5) RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список тригерров /trigger')
            if message.reply_to_message.content_type == "photo":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow('''SELECT tg_name FROM test.public.triggers_chat WHERE tg_name = $1 and id_chat=$2''', *arg,)
                reply_photo_id = message.reply_to_message.photo[-1].file_id
                reply_caption = message.reply_to_message.caption
                arg = 'фото', name_trigger, reply_photo_id, message.chat.id, message.from_user.id, reply_caption
                if find_tg:
                    if await pool.fetchval('''UPDATE test.public.triggers_chat SET tg_photo=$3,user_add=$5, tg_type=$1, tg_text=$6 WHERE tg_name=$2 and user_add=$5 and id_chat = $4 RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список тригерров /trigger')
                else:
                    if await pool.fetchval('''INSERT INTO test.public.triggers_chat (tg_type, tg_name , tg_photo, id_chat, user_add, tg_text) VALUES ($1,$2,$3,$4,$5,$6) RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список тригерров /trigger')
            if message.reply_to_message.content_type == "audio":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow('''SELECT tg_name FROM test.public.triggers_chat WHERE tg_name = $1 and id_chat=$2''', *arg,)
                reply_audio_id = message.reply_to_message.audio.file_id
                reply_caption = message.reply_to_message.audio.title
                arg = 'аудио', name_trigger, reply_audio_id, message.chat.id, message.from_user.id, reply_caption
                if find_tg:
                    if await pool.fetchval('''UPDATE test.public.triggers_chat SET tg_audio=$3,user_add=$5, tg_type=$1, tg_text=$6 WHERE tg_name=$2 and user_add=$5 and id_chat = $4 RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список тригерров /trigger')
                else:
                    if await pool.fetchval('''INSERT INTO test.public.triggers_chat (tg_type, tg_name , tg_audio, id_chat, user_add, tg_text) VALUES ($1,$2,$3,$4,$5,$6) RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список тригерров /trigger')
            if message.reply_to_message.content_type == "sticker":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow('''SELECT tg_name FROM test.public.triggers_chat WHERE tg_name = $1 and id_chat=$2''', *arg,)
                reply_sticker_id = message.reply_to_message.sticker.file_id
                arg = 'стикер', name_trigger, reply_sticker_id, message.chat.id, message.from_user.id
                if find_tg:
                    if await pool.fetchval('''UPDATE test.public.triggers_chat SET tg_sticker=$3,user_add=$5, tg_type=$1 WHERE tg_name=$2 and user_add=$5 and id_chat = $4 RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список тригерров /trigger')
                else:
                    if await pool.fetchval('''INSERT INTO test.public.triggers_chat (tg_type, tg_name , tg_sticker, id_chat, user_add) VALUES ($1,$2,$3,$4,$5) RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список тригерров /trigger')
            if message.reply_to_message.content_type == "video":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow('''SELECT tg_name FROM test.public.triggers_chat WHERE tg_name = $1 and id_chat=$2''', *arg,)
                reply_video_id = message.reply_to_message.video.file_id
                reply_text = message.reply_to_message.caption
                arg = 'видео', name_trigger, reply_video_id, message.chat.id, message.from_user.id, reply_text
                if find_tg:
                    if await pool.fetchval('''UPDATE test.public.triggers_chat SET tg_video=$3,user_add=$5, tg_type=$1, tg_text=$6 WHERE tg_name=$2 and user_add=$5 and id_chat = $4 RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список тригерров /trigger')
                else:
                    if await pool.fetchval('''INSERT INTO test.public.triggers_chat (tg_type, tg_name , tg_video, id_chat, user_add, tg_text) VALUES ($1,$2,$3,$4,$5,$6) RETURNING TRUE''', *arg):
                        await message.answer(f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список тригерров /trigger')

        except:
            await message.answer('призошла ошибка')


@rate_limit(1, 'del_trigger')
@dp.message_handler(commands='trigger',
                    chat_type=[types.ChatType.GROUP,types.ChatType.SUPER_GROUP],
                    is_chat_admin=True,
                    commands_prefix='-')
async def bot_trigger_add_or_update(message: types.Message):
    if message.text != '-trigger':
        try:
            pool: Connection = db
            name_trigger = message.text.split('-trigger', maxsplit=1)[1].strip()
            arg = name_trigger, message.chat.id
            find_tg = await pool.fetchval('''SELECT id FROM test.public.triggers_chat WHERE tg_name = $1 and id_chat=$2''', *arg,)
            if find_tg:
                if await pool.fetchrow('''delete from test.public.triggers_chat WHERE id=$1 RETURNING TRUE''', find_tg,):
                    await message.answer(f'триггер <b>{name_trigger}</b> был удалён')
                else:
                    await message.answer(f'Произошла ошибка, не смог удалить триггер {name_trigger}')
            else:
                await message.answer('Такого тригерра не существует')
        except Exception as err:
            await message.answer(f'призошла ошибка {err}')


@rate_limit(2, 'trigger_list')
@dp.message_handler(commands='trigger',
                    chat_type=[types.ChatType.GROUP,types.ChatType.SUPER_GROUP],
                    commands_prefix='/')
async def bot_trigger_add_or_update(message: types.Message):
    try:
        pool: Connection = db
        find_tg: Record = await pool.fetch('''SELECT tg_name, tg_type FROM test.public.triggers_chat WHERE id_chat=$1''', message.chat.id,)
        list_tg =[]
        if find_tg:
            for item in find_tg:
                list_tg.append(f'<b>{item["tg_name"]}</b>: {item["tg_type"]}')
            await message.answer(f'Список триггеров:\n'+ "\n".join(list_tg))
        else:
            await message.answer('Триггеры отсутствуют!\nЧто бы добавить триггер\n+trigger <b>имя триггера</b> ответом на сообщение')

    except Exception as err:
        await message.answer(f'призошла ошибка {err}')