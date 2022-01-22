from aiogram import types

from keyboards.inline.boosters_kb import create_cb_boosters
from loader import dp, db
from aiogram.utils.emoji import emojize
from utils.misc import rate_limit
from asyncpg import Connection, Record


@rate_limit(2, 'boosters')
@dp.message_handler(commands='boosters')
async def bot_boosters_check(message: types.Message):
    try:
        pool: Connection = db
        find_user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', message.from_user.id,)
        if find_user:
            anws = ''
            list_anws =["""Есть 3 типа мау (мявка)

🀄Голиаф 🛡Защита: 0.25%
🀄️Балиста ⚔️Урон: 0.25%
🀄️Гастрафет 💨Уворот: 0.25%""", '4 модуля (🀄️Оружейный модуль, 🀄️Модуль брони, 🀄️Модуль ускорителя, 🀄️Модуль питания)','☣️Ядерная энергия',"""Есть 4 анимуса

🎴Пеймон 🛡Защита: 0.25%
🎴Изида ⚔️Урон: 0.25% 
🎴Геката 💨Уворот: 0.25%
🎴Инанна ❤️Здоровье: 0.25%""",'4 части (🎴Магия, 🎴Крылья, 🎴Аура, 🎴Энергетический камень)','🏺Потусторонняя энергия',"""Есть 3 ПУ (пусковая установка)

🃏Ракетница 🛡Защита: 0.25%
🃏Огнемет ⚔️Урон: 0.25% (оч странно, должна же быть изидиа🤨)
🃏Пулемет 💨Уворот: 0.25%""",'4 части (🃏Дуло, 🃏Осадный корпус, 🃏Маскировка, 🃏Боеприпасы)',' ⚗️Темная материя']
            if find_user["race"] == 1:
                anws = f"""Данная команда поможет быстрее определится, какие усиления тебе нужны!

{list_anws[0]}

Что бы их собрать требуется 🏵1 400 000 адены и {list_anws[1]}

Надев, у тебя появится 4 доп слота для усилений

И да, что бы надеть или починить части, требуется {list_anws[2]}

Ниже можешь выбрать нужный слот и где он должен работать для быстрого поиска
"""
            elif find_user["race"] == 2:
                anws = f"""Данная команда поможет быстрее определится, какие усиления тебе нужны!

{list_anws[3]}

Что бы её собрать требуется 🏵1 400 000 адены и {list_anws[4]}

Надев, у тебя появится 4 доп слота для усилений

И да, что бы надеть или починить части, требуется {list_anws[5]}

Ниже можешь выбрать нужный слот и где он должен работать для быстрого поиска
"""

            elif find_user["race"] == 3:
                anws = f"""Данная команда поможет быстрее определится, какие усиления тебе нужны!

{list_anws[6]}

Что бы её собрать требуется 🏵1 400 000 адены и {list_anws[7]}

Надев, у тебя появится 4 доп слота для усилений

И да, что бы надеть или починить части, требуется {list_anws[8]}

Ниже можешь выбрать нужный слот и где он должен работать для быстрого поиска
"""
            await message.answer(text=anws, reply_markup=await create_cb_boosters(message.from_user.id, message.date, find_user["race"]))
        else:
            await message.answer('извини, но я тебя не знаю, скинь свой профиль из игры, чтобы я смог понять к какой ты расе принадлежишь')
    except Exception as ee:
        await message.answer(emojize(ee))





