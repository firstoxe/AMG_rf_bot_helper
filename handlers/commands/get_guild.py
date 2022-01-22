from aiogram import types
from loader import dp, db
from asyncpg import Connection, Record
from aiogram.utils.emoji import emojize, demojize
from utils.misc import rate_limit


@rate_limit(3, 'get_guild')
@dp.message_handler(commands='get_guild')
async def bot_command_get_user(message: types.Message):
    pool: Connection = db
    try:
        guild: Record = await pool.fetch('''
        SELECT lvl,guild,nickname,id 
        from test.public."user" 
        where guild=$1 and last_activity + interval '30 day' > now() ''', demojize(message.text).split(' ', maxsplit=1)[1],)
        ls = []
        for item in guild:
            ls.append(f'<b>[{str(item[0])}]</b>[{str(item[1])}]<a href="tg://user?id={str(item[3])}">{str(item[2])}</a>')
        def keyFunc(item):
            return int(item.split('[', maxsplit=1)[1].split(']',maxsplit=1)[0])
        ls.sort(key=keyFunc, reverse=True)
        #ls.insert(0,f'Члены гильдии - {message.text.split(" ")[1]}\n')
        await message.reply(emojize(f'Члены гильдии - <b>{message.text.split(" ")[1]}</b>\n\n'+'\n'.join(["{}) {!s}".format(i, s) for i, s in enumerate(ls, 1)])))
        #await message.reply(emojize('\n'.join(ls)))

    except:
        await message.answer(f'Команда использована не правильно.\n'
                             f'Пример - /get_guild 13')

