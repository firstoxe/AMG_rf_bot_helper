from aiogram import types

from keyboards.inline.work_kb import create_cb_work_resource_sel
from loader import dp, db
from aiogram.utils.emoji import emojize, demojize
from utils.misc import rate_limit
from asyncpg import Connection, Record


@rate_limit(2, 'test121')
@dp.message_handler(commands='test111', chat_type=types.ChatType.PRIVATE)
async def bot_work_take(message: types.Message):
    pool: Connection = db
    all_chats = await pool.fetch('''SELECT * FROM test.public.cave_all_chat''')
    for item in all_chats:
        msg = await message.bot.send_message(chat_id=item["id_chat"],
                                             text="Небольшое изменение в работе бота\n\n"
                                                  "Может не увидеть ваш подъём или спуск из пещеры!\n\n"
                                                  "Совершите любое действие отображаемое в @rf_action или обновите "
                                                  "профиль, если уже в пещере то обновите профиль"
                                                  "")
        await msg.pin()
