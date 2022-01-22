from aiogram import types
from datetime import timedelta, datetime

from loader import dp, db
from aiogram.utils.emoji import emojize, demojize
from utils.misc import rate_limit
from asyncpg import Connection, Record


@rate_limit(2, 'work')
@dp.message_handler(is_work_contract=True, is_from_rf_bot=True, chat_type=types.ChatType.PRIVATE)
async def bot_work_take(message: types.Message):
    pool: Connection = db
    find_user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', message.from_user.id,)
    if message.forward_date + timedelta(days=1) > datetime.now():
        if find_user:
            if find_user["lvl"]>37:
                if await pool.fetchval('''SELECT count(id) FROM test.public.contract WHERE user_id = $1''', message.from_user.id,) < 6:
                    for item in demojize(message.text).splitlines():
                        if item.find('Ресурс: ') != -1:
                            resource = item.split('Ресурс: ')[1]
                            if item.find('Ядерная') != -1:
                                race = 1
                            elif item.find('Потусторонняя') != -1:
                                race = 2
                            elif item.find('Темная') != -1:
                                race = 3
                        if item.find('Количество: ') != -1:
                            amount = int(item.split('Количество: ')[1].split('ед')[0])
                        if item.find('Стоимость одной единицы: ') != -1:
                            price = int(item.split('Стоимость одной единицы: ')[1].replace(' ', ''))
                        if item.find('Принять контракт - ') != -1:
                            link = item.split('Принять контракт - ')[1]
                    find_contract: Record = await pool.fetchrow('''SELECT link FROM test.public.contract WHERE link = $1''', link,)
                    if find_contract:
                        await message.answer('Этот контракт уже присутствует в базе!')
                    else:
                        arg = resource, amount, race, price, link, find_user["id"], find_user["guild"], find_user["nickname"], message.forward_date
                        if await pool.fetchval('''INSERT INTO test.public.contract (resourse, amount, race_res, price, link, user_id, user_guild, user_nickname, date_msg) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING TRUE''', *arg):
                            await message.answer(f'Контракрт успешно добавлен в базу')
                        else:
                            await message.answer('Не смог добавить контракт!')
                else:
                    await message.answer('Ты можешь добавить только 5 контрактов')
            else:
                await message.answer('извини, но я тебя не знаю, скинь свой профиль из игры')
        else:
            await message.answer('Не воруй чужие контракты =)')
    else:
        await message.answer('Контракт слишком старый, его нельзя добавить')
