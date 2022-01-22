from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime


dat_boosters_sel_slot = CallbackData('boosters_slot', 'action', 'id', 'date', 'race')

async def create_cb_boosters(id, date, race):
    kb = InlineKeyboardMarkup(row_width=2)
    pool: Connection = db
    all_slot_race: Record = await pool.fetch("""SELECT name_slot,slot_id from test.public.boosters_slot where race = $1 order by slot_id""", int(race),)
    kb.add(InlineKeyboardButton(all_slot_race[0][0], callback_data=dat_boosters_sel_slot.new(str(all_slot_race[0][1]),str(id),str(date).replace(':',';'),str(race))),
           InlineKeyboardButton(all_slot_race[1][0], callback_data=dat_boosters_sel_slot.new(str(all_slot_race[1][1]),str(id),str(date).replace(':',';'),str(race))))
    kb.add(InlineKeyboardButton(all_slot_race[2][0], callback_data=dat_boosters_sel_slot.new(str(all_slot_race[2][1]),str(id),str(date).replace(':',';'),str(race))),
           InlineKeyboardButton(all_slot_race[3][0], callback_data=dat_boosters_sel_slot.new(str(all_slot_race[3][1]),str(id),str(date).replace(':',';'),str(race))))
    return kb


dat_boosters_sel_type = CallbackData('boosters_type', 'action', 'id', 'date', 'race', 'slot')


async def create_cb_boosters_type(id, date,race,slot):
    kb = InlineKeyboardMarkup(row_width=2)
    pool: Connection = db
    all_marker: Record = await pool.fetch("""SELECT name,id from test.public.boosters_loc order by id""")
    kb.add(InlineKeyboardButton(all_marker[0][0], callback_data=dat_boosters_sel_type.new(str(all_marker[0][1]),str(id),str(date).replace(':',';'),str(race),slot)),
           InlineKeyboardButton(all_marker[1][0], callback_data=dat_boosters_sel_type.new(str(all_marker[1][1]),str(id),str(date).replace(':',';'),str(race),slot)))
    kb.add(InlineKeyboardButton(all_marker[2][0], callback_data=dat_boosters_sel_type.new(str(all_marker[2][1]),str(id),str(date).replace(':',';'),str(race),slot)),
           InlineKeyboardButton(all_marker[3][0], callback_data=dat_boosters_sel_type.new(str(all_marker[3][1]),str(id),str(date).replace(':',';'),str(race),slot)))
    kb.add(InlineKeyboardButton('Выбрать слот', callback_data=dat_boosters_sel_type.new('back',str(id),str(date).replace(':',';'),str(race),slot)))
    return kb




@dp.callback_query_handler(dat_boosters_sel_slot.filter(action=['1', '2', '3', '4']))
async def inline_kb_update_boosters_sel_slot(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            anws = """<b>Выбери территории, в которых он будет работать</b>
            
        <b>Есть 4 вида территорий:</b>

    <b>Война</b> 
👩‍🚀Иса,Гебо,Зиг,🧝‍♀Исс,Дагаз,Хагал,🤖Тир,Эйви,Беркана,👩‍🚀🧝‍♀🤖Терминалы,🦖Хран,🌋Краговые шахты

    <b>Замки</b> 
🕌Нова,🕌Мира,🕌Антарес,🕌Арэс,🕌Фобос,🕌Торн,🕌Кастор,🕌Алькор,🕌Гром,🕌Конкорд,🏯Беллатрикс,🏯Иерихон,🏯Цефея,🏯Супер нова,🏰Альдебаран,🏰Бетельгейзе

    <b>Локации</b> 
🐣Окрестности Ген. штаба,🐥Аванпост,🦅Колония Харам,🏜Сеттовая пустыня,🍀Элан,🦇Земли Изгнанников,🏔Этер

    <b>Пещеры</b> 
🗻Пещера №1-10

Прочность модулей тратиться при каждом бое, если модуль срабатывает в этом месте
"""
            await query.bot.edit_message_text(text=anws,
                                                    chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_boosters_type(callback_data["id"],callback_data_time,callback_data["race"],callback_data["action"]))
            await query.answer(cache_time=2)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=5)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /boosters для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)



@dp.callback_query_handler(dat_boosters_sel_type.filter(action=['back']))
async def inline_kb_update_boosters_sel_slot(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
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
            if int(callback_data["race"]) == 1:
                anws = f"""Данная команда поможет быстрее определится, какие усиления тебе нужны!

{list_anws[0]}

Что бы её собрать требуется 🏵1 400 000 адены и {list_anws[1]}

Надев, у тебя появится 4 доп слота для усилений

И да, что бы надеть или починить части, требуется {list_anws[2]}

Ниже можешь выбрать нужный слот и где он должен работать для быстрого поиска
"""
            elif int(callback_data["race"]) == 2:
                anws = f"""Данная команда поможет быстрее определится, какие усиления тебе нужны!

{list_anws[3]}

Что бы их собрать требуется 🏵1 400 000 адены и {list_anws[4]}

Надев, у тебя появится 4 доп слота для усилений

И да, что бы надеть или починить части, требуется {list_anws[5]}

Ниже можешь выбрать нужный слот и где он должен работать для быстрого поиска
"""

            elif int(callback_data["race"]) == 3:
                anws = f"""Данная команда поможет быстрее определится, какие усиления тебе нужны!

{list_anws[6]}

Что бы её собрать требуется 🏵1 400 000 адены и {list_anws[7]}

Надев, у тебя появится 4 доп слота для усилений

И да, что бы надеть или починить части, требуется {list_anws[8]}

Ниже можешь выбрать нужный слот и где он должен работать для быстрого поиска
"""
            await query.bot.edit_message_text(text=anws,
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id,
                                              reply_markup=await create_cb_boosters(callback_data["id"],callback_data_time,callback_data["race"]))
            await query.answer(cache_time=2)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=5)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /boosters для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)


@dp.callback_query_handler(dat_boosters_sel_type.filter(action=['1', '2', '3', '4']))
async def inline_kb_update_boosters_sel_type(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            pool: Connection = db
            arg = int(callback_data["race"]), int(callback_data["slot"]), int(callback_data["action"])
            all_boost: Record = await pool.fetch("""SELECT * from test.public.boosters where race=$1 and slot_id=$2 and marker_type=$3 """, *arg)
            if all_boost:
                list_boost =[]
                for item in all_boost:
                    list_boost.append(emojize(f'[{item["lvl"]}]<b>{item["name"]}</b>(🧱{item["durability"]} 🔄{item["repair_price"]}): {item["stats"] if item["stats"] else ""}\n{item["features"]if item["features"] else ""}'))
                arg = int(callback_data["race"]), int(callback_data["slot"])
                await query.bot.edit_message_text(text=f'<b>Вот список всего, что есть для слота <code>{await pool.fetchval("""SELECT name_slot from test.public.boosters_slot where race =$1 and slot_id=$2""", *arg)}</code>:</b>\n\n'+'\n\n'.join(list_boost),
                                                  chat_id=query.message.chat.id,
                                                  message_id=query.message.message_id,
                                                  reply_markup=await create_cb_boosters_type(callback_data["id"],callback_data_time,callback_data["race"],callback_data["slot"]))
                await query.answer(cache_time=2)
            else:
                await query.bot.edit_message_text(text='Извини, но ничего нету =)',
                                                  chat_id=query.message.chat.id,
                                                  message_id=query.message.message_id,
                                                  reply_markup=await create_cb_boosters_type(callback_data["id"],callback_data_time,callback_data["race"],callback_data["slot"]))
                await query.answer(cache_time=2)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=5)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /boosters для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)