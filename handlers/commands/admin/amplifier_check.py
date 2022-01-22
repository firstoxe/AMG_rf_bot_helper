import asyncio
from aiogram import types
from loader import dp, db
from aiogram.utils.emoji import demojize,emojize
from utils.misc import rate_limit
from data.config import admins
from asyncpg import Connection, Record


@rate_limit(0, 'amplifier')
@dp.message_handler(user_id=admins, chat_type="private", is_from_rf_bot=True, is_amplifier=True)
async def bot_boosters_check(message: types.Message):
    try:
        pool: Connection = db
        boost_amp=None
        cloc_amp=None
        for item in demojize(message.text).splitlines():
            if item.find('Название: ') != -1:
                name_amp = item.split(':')[3]
            if item.find('Уровень: ') != -1:
                lvl_amp = int(item.split('Уровень: ')[1])
            if item.find('Раса: ') != -1:
                if item.find('Basilaris') != -1:
                    race_amp = 1
                elif item.find('Castitas') != -1:
                    race_amp = 2
                elif item.find('Aquilla') != -1:
                    race_amp = 3
            if item.find('Прочность: ') != -1:
                durability_amp = int(item.split('Прочность: ')[1])
            if item.find('Ремонт 1ед. прочности: ') != -1:
                repair_amp = int(item.split('Ремонт 1ед. прочности: ')[1].replace(' ',''))
            if item.find('Надевается в слот: ') != -1:
                slot_amp = await pool.fetchval('''SELECT slot_id FROM test.public.boosters_slot WHERE name_slot = $1''', item.split('Надевается в слот: ')[1],)
            if item == 'Характеристики:':
                boost_amp=[]
                flags= False
                for item2 in demojize(message.text).splitlines():
                    if item2 != '' and flags:
                        boost_amp.append(item2)
                    if item2 == 'Характеристики:':
                        flags = True
                    if item2 == '' and flags:
                        break
            if item == 'Особенности работы:':
                cloc_amp=[]
                flags= False
                for item2 in demojize(message.text).splitlines():
                    if item2 != '' and flags:
                        cloc_amp.append(item2)
                    if item2 == 'Особенности работы:':
                        flags = True
                    if item2 == '' and flags:
                        break
            if item.find('Работает на локациях: ') != -1:
                loc_work_amp = item.split('Работает на локациях: ')[1]
                if item.find('Краговые шахты') !=-1:
                    marker_type_amp=1
                if item.find('Кастор') !=-1:
                    marker_type_amp=2
                if item.find('Пещера') !=-1:
                    marker_type_amp=4
                if item.find('Колония Харам') !=-1:
                    marker_type_amp=3
        if boost_amp:
            boost_amp = "\n".join(boost_amp)
        if cloc_amp:
            cloc_amp = "\n".join(cloc_amp)

        find_module: Record = await pool.fetchrow('''SELECT name FROM test.public.boosters WHERE name = $1''', name_amp,)
        arg = name_amp,lvl_amp,race_amp,durability_amp,repair_amp,slot_amp,boost_amp,cloc_amp,loc_work_amp,marker_type_amp
        if find_module:
            if await pool.fetchval('''UPDATE test.public.boosters SET name=$1, lvl=$2, race=$3, durability=$4, repair_price=$5, slot_id=$6, stats=$7, features=$8,location=$9,marker_type=$10 where name = $1 RETURNING TRUE''', *arg):
                await message.answer(f'Модуль обновлён')
        else:
            if await pool.fetchval('''INSERT INTO test.public.boosters (name, lvl, race, durability, repair_price, slot_id, stats, features, location, marker_type) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) RETURNING TRUE''', *arg):
                await message.answer(f'Модуль добавлен')
    except Exception as ee:
        await message.answer(emojize(ee))





