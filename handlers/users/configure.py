from aiogram import types
from loader import dp, db
from aiogram.types.chat import ChatType
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import demojize, emojize
from data.config import admins
from utils.misc import rate_limit
from keyboards.inline.config_user import create_cb_user


@rate_limit(3, 'config')
@dp.message_handler(chat_type=['private'], commands='config')
async def bot_command_get_user(message: types.Message):

    await message.answer(emojize(f"""<b>⚙️Настроечки</b>

:performing_arts:<b>Данжи</b> - > получение приглашений в данжи
:performing_arts:<b>Пещеры</b> - > получение приглашений в пещеры
:performing_arts:<b>Только ГИ</b> - > получение приглашений в данжи только от своей ги

:dagger:<b>ЧВ</b> - > напоминание о начале ЧВ за 15 минут

:oncoming_fist_light_skin_tone:<b>Арена</b> - > напоминание о арене за 10 мин и при начале
    
:mountain_cableway:<b>Вход/Выход из пещер</b> - > уведомления о поднятии и спуске в пещерах из твоей лиги

:counterclockwise_arrows_button:<b>Обновления бота</b> - > новости с обновлениями бота

:T-Rex:<b>Страж</b> - > сообщает о появлении стража и началом его атаки

:classical_building:<b>Пинг не в гш</b> - > разрешает пинговать в личное сообщенние, если не в ген. штабе
    
    """), reply_markup=await create_cb_user(message.from_user.id))
