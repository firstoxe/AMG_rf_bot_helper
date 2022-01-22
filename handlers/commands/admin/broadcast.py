import asyncio
import logging

from aiogram import types
from aiogram.utils import exceptions
from asyncpg import Connection, Record

from data.config import admins
from filters.work_with_user import helper_user
from loader import dp, db
from utils.misc import rate_limit


@rate_limit(0, 'update')
@dp.message_handler(user_id=admins, chat_type="private", commands='update')
async def broadcaster(message: types.Message):
    #запрос в базу всех пользователей с диалогом
    pool: Connection = db
    list_user: Record = await pool.fetch('''SELECT id,lvl,guild,nickname 
    from test.public."user" 
    inner join test.public.notify n on "user".id = n.id_user where bot_update=TRUE''' )
    count = 0
    try:
        for user in list_user:
            if await send_message(user, message):
                count += 1
            await asyncio.sleep(.07)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")
    await message.answer(f'Сообщение об обновлении доставлено <b>{count}</b> пользователям*')



async def send_message(user: Record, message: types.Message, disable_notification: bool = False) -> bool:
    try:
        pool: Connection = db
        logging.info(f"Target [ID:{user['id']}]")
        await message.bot.send_message(user["id"], f'Приветствую {await helper_user(user["id"])}'
        f'\n\n{message.text.split(" ", maxsplit=1)[1]}', disable_notification=disable_notification)
        arg = True, user["id"]
        await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)

    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user['id']}]: blocked by user")
        arg = False, user["id"]
        await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user['id']}]: invalid user ID")

        arg = False, user["id"]
        await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user['id']}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user, message)  # Recursive call
    except exceptions.UserDeactivated:
        arg = False, user["id"]
        await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)
        logging.error(f"Target [ID:{user['id']}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user['id']}]: failed")
    except exceptions.CantInitiateConversation:
        logging.exception(f"Target [ID:{user['id']}]: не начинал диалога!")
    except Exception as err:
        logging.exception(f"Target [ID:{user['id']}]: ошибка {err}!")
    else:
        logging.info(f"Target [ID:{user['id']}]: success")
        return True
    return False