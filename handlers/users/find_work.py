from aiogram import types

from keyboards.inline.work_kb import create_cb_work_resource_sel
from loader import dp, db
from aiogram.utils.emoji import emojize, demojize
from utils.misc import rate_limit
from asyncpg import Connection, Record


@rate_limit(2, 'find_contract')
@dp.message_handler(commands='find_contract', chat_type=types.ChatType.PRIVATE)
async def bot_work_take(message: types.Message):
    pool: Connection = db
    find_user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', message.from_user.id,)
    if find_user:
        if find_user["lvl"] > 37:
            work_time_dict = {1: 15, 2: 9, 3: 4, 4: 2, 5: 1}

            await message.answer(f'Здесь ты можешь найти заказы на работу\n'
                                 f'\n'
                                 f'<b>Твоя скорость работы:</b>\n'
                                 f'☣️Ядерная энергия - {work_time_dict[find_user["lvl_prof_bel"]]}ч.\n'
                                 f'🏺Потусторонняя энергия - {work_time_dict[find_user["lvl_prof_cor"]]}ч.\n'
                                 f'⚗️Темная материя - {work_time_dict[find_user["lvl_prof_acr"]]}ч.\n\n'
                                 f''
                                 f'Количество заказов в базе - {await pool.fetchval("SELECT count(link) from test.public.contract")}\n'
                                 f'☣️ - {await pool.fetchval("SELECT count(link) from test.public.contract where race_res=1")}\n'
                                 f'🏺 - {await pool.fetchval("SELECT count(link) from test.public.contract where race_res=2")}\n'
                                 f'⚗️ - {await pool.fetchval("SELECT count(link) from test.public.contract where race_res=3")}\n\n'
                                 f''
                                 f'Выбери тип ресурса',
                                 reply_markup=await create_cb_work_resource_sel(message.from_user.id, message.date))

        else:
            await message.answer('Твой уровень слишком маленький, для работы требуется минимум 38 уровень')
    else:
        await message.answer('извини, но я тебя не знаю, скинь свой профиль из игры')
