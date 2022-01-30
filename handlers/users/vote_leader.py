import re
from aiogram import types
from loader import dp, db
from aiogram.utils.text_decorations import html_decoration
from aiogram.utils.emoji import demojize, emojize
from data.config import admins
from re import sub
from asyncpg import Record, Connection
from filters.guild_check import check_g
from utils.misc import rate_limit
from handlers.commands.recipe.item import stat_for_item


@rate_limit(0, 'vote_leader')
@dp.message_handler(vote_leader=True)
async def bot_anw_vote_leader(message: types.Message):
    msg = message.text.splitlines()
    msg.sort(key=lambda x: float(x.split(' | ')[3][:-1]), reverse=True)

    def toFixed(numObj, digits=2):
        return float(f"{numObj:.{digits}f}")

    if float(msg[0].split(' | ')[3][:-1]) > 0:

        find_min = float(msg[0].split(' | ')[3][:-1])

        def cyc(golos=0):
            max = 0
            golos += 1
            test = 0.0
            while max <= 300:
                max += 1
                test = toFixed(float(golos / max * 100))
                if test != find_min and max >= 300:
                    break
                if test == find_min:
                    return find_min / golos
            if max >= 300 and test != find_min:
                return toFixed(cyc(golos))
            if test == find_min:
                return find_min / golos
    golos = cyc()
    new_list = []
    for item in msg:
        if float(item.split(' | ')[3][:-1]) > 0:
            new_list.append(item + ' - ' + str(int(toFixed(float(item.split(' | ')[3][:-1]) / golos, 0))) + '🗳')
        else:
            new_list.append(item + ' - 0🗳')

    aws = f"""👑Патриарх: {new_list[0].split(' | ')[0].split(')', maxsplit=1)[1]} - {new_list[0].split(' | ')[3].split(' - ')[1]}
🔱Архонт: {new_list[1].split(' | ')[0].split(')', maxsplit=1)[1]} - {new_list[1].split(' | ')[3].split(' - ')[1]}
🗡Атакующий: {new_list[2].split(' | ')[0].split(')', maxsplit=1)[1]} - {new_list[2].split(' | ')[3].split(' - ')[1]}
🛡Защитник: {new_list[3].split(' | ')[0].split(')', maxsplit=1)[1]} - {new_list[3].split(' | ')[3].split(' - ')[1]}
📯Поддержка: {new_list[4].split(' | ')[0].split(')', maxsplit=1)[1]} - {new_list[4].split(' | ')[3].split(' - ')[1]}
============================="""

    if len(new_list) > 5:
        for item in new_list:
            if new_list.index(item) > 4:
                aws += f"\n {item.split(' | ')[0].split(')', maxsplit=1)[1]}"
    aws += f"\n=============================\nЦена 1🗳 = {golos}%"
    await message.reply(aws)
    await message.delete()
