from aiogram import types
from loader import dp, db
from filters.totem_update_filter import TotemUpdateFilter
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import demojize, emojize
from utils.misc import rate_limit

list_bronze = [0, 5, 15, 30, 70, 120, 250, 340, 500, 650, 1300, 2275]
list_silver = [0, 1, 5, 20, 50, 100, 200, 280, 400, 500, 1000, 1750]
list_gold = [0, 0, 1, 5, 30, 50, 110, 200, 300, 420, 840, 1470]
list_aden = [50000, 100000, 300000, 500000, 1000000, 2000000, 4000000, 6000000, 8000000, 10000000, 20000000, 37500000]
list_lvl_ares = [3, 5, 7, 9, 11, 13, 16, 20, 24, 28, 32, 36]
list_lvl_poseidon = [2.5, 5, 7.5, 9, 11, 14, 17, 20, 24, 28, 31.5, 35]
list_lvl_kronos = [5, 8, 11, 15, 21, 26, 31, 36, 43, 50, 55, 60]
list_lvl_ge_de_ze = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
list_nalog = [
    [
        [8, 12], [6, 8], [4, 6], [175000, 250000]
    ],
    [
        [6, 8], [4, 7], [3, 4], [75000, 150000]
    ]
]
list_totem_name = {'Ареса': 'atk', 'Посейдона': 'def', 'Кроноса': 'hp',
                   'Гефеста': 'dodge', 'Зевса': 'crit', 'Деймоса': 'acc'}


@rate_limit(0, 'user_totem_update')
@dp.message_handler(TotemUpdateFilter())
async def user_totem_update(message: types.Message):
    if (datetime.now() - message.forward_date).total_seconds() < 6000:
        var_str = demojize(message.text).splitlines()
        if var_str[0].find('Максимальный уровень тотема') == -1:
            totem_lvl = int(var_str[1].split(' - ')[1][:-3])
            for item in var_str:
                if item.find('Ежедневное подношение') == -1 and item.find('Чтобы восславить тотем этого бога') == -1:
                    if item.find('Аден: :rosette:') != -1:
                        aden = int(item.split('/')[0].split('Аден: :rosette:')[1].replace(' ', ''))
                    if item.find(':3rd_place_medal:') != -1:
                        bronze = int(item.split('/')[0].split(':3rd_place_medal:')[1].replace(' ', ''))
                    if item.find(':2nd_place_medal:') != -1:
                        silver = int(item.split('/')[0].split(':2nd_place_medal:')[1].replace(' ', ''))
                    if item.find(':1st_place_medal:') != -1:
                        gold = int(item.split('/')[0].split(':1st_place_medal:')[1].replace(' ', ''))
                    if item.find('Припасы для ежедневного пожертвования:') != -1:
                        break
        elif var_str[0].find('Максимальный уровень тотема') != -1:
            totem_lvl = 12
            aden = 0
            bronze = 0
            silver = 0
            gold = 0
        pool: Connection = db
        arg = totem_lvl,aden,bronze,silver,gold, message.from_user.id

        for item in list_totem_name:
            if item in var_str[1] or item in var_str[3]:
                await pool.fetch('''UPDATE test.public.totems SET {0}=$1, {0}_a=$2, {0}_b=$3, {0}_s=$4, {0}_g=$5 WHERE id_user=$6'''.format(list_totem_name[item]), *arg)
                break
        user_nick: Record = await pool.fetchrow('''SELECT nickname FROM test.public."user" 
                                            WHERE id = $1''', message.from_user.id,)
        if var_str[0].find('Максимальный уровень тотема') == -1:
            await message.answer(emojize(f"<a href='tg://user?id={message.from_user.id}'>{emojize(user_nick[0])}</a>\n{var_str[1].split(' - ')[0]} обновлён"))
        elif var_str[0].find('Максимальный уровень тотема') != -1:
            await message.answer(emojize(f"<a href='tg://user?id={message.from_user.id}'>{emojize(user_nick[0])}</a>\n{var_str[3].split(' - ')[0]} обновлён"))
    else:
        pool: Connection = db
        user_nick: Record = await pool.fetchrow('''SELECT nickname FROM test.public."user" 
                                            WHERE id = $1''', message.from_user.id,)
        await message.answer(f'<a href="tg://user?id={message.from_user.id}">{emojize(user_nick[0])}</a>\nПрошло больше 100 мин! Давай посвежее =)')
    if message.from_user.id == message.chat.id:
        await message.delete()
    else:
        try:
            await message.delete()
        except:
            await message.answer('Не достаточно прав для удаления сообщения!')