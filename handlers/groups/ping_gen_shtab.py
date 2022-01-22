from aiogram import types
from filters.ping_none_gen_shtab import PingNoneGenShtab
from loader import dp, db
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import demojize, emojize


race_find = {':woman_astronaut:': 1, ':woman_elf:': 2, ':elf:‍:female_sign:': 2, ':robot:': 3}


@dp.message_handler(PingNoneGenShtab())
async def bot_forward_not_in_gen_shtab(message: types.Message):
    if(datetime.now() - message.forward_date).seconds <= 3600:
        pool: Connection = db
        msg = demojize(message.text)[1:]
        ping = bool
        list_re = [' не в ген. штабе]',' уже совершает действие]',' выполняют другое действие]',' выполняет другое действие]']
        for item in list_re:
            if msg.find(item) != -1:
                msg = msg.split(item, maxsplit=1)[0]
                break
        if message.chat.id != message.from_user.id:
            ping = False
        elif message.chat.id == message.from_user.id:
            ping = True
        if msg.count(',') > 0:
            msg = msg.split(', ')
            tmp = msg
            msg = []
            for item in tmp:
                for key in race_find:
                    if str(item).find(key) != -1:
                        var_tmp = item.split(key)[1]
                        if var_tmp.find('[') != -1 and var_tmp.find(']') != -1 and var_tmp.find(']') < len(var_tmp)-1:
                            msg.append(item.split(key)[1].split(']', maxsplit=1)[1])
                        else:
                            msg.append(item.split(key)[1])
        else:
            for key in race_find:
                if str(msg).find(key) != -1:
                    if str(msg).find('[') != -1 and str(msg).find(']') != -1 and str(msg).find(']') < len(str(msg))-1:
                        msg = [str(msg).split(key)[1].split(']', maxsplit=1)[1]]
                    else:
                        msg = str(msg).split(key)[1]

                    break

        if ping:
            record: Record = await pool.fetch('''SELECT test.public."user".id,guild,nickname from test.public."user"
                                                 INNER JOIN test.public.notify n on "user".id = n.id_user
                                    WHERE user_dialog = TRUE and ping_pm = TRUE and nickname= any($1::text[])''', msg)
            list_suck = ''
            list_dinaid = ''
            for item in record:
                if item[1] is None:
                    list_suck = (f'{list_suck}:check_mark_button:[{item[1]}]'
                                 f'<a href="tg://user?id={item[0]}">{item[2]}</a>\n')
                else:
                    list_suck = f'{list_suck}:check_mark_button:<a href="tg://user?id={item[0]}">{item[2]}</a>\n'
                await message.bot.send_message(item[0], 'Пати лидер просит тебя вернуться в ген. штаб!')

            record: Record = await pool.fetch('''SELECT test.public."user".id,guild,nickname from test.public."user"
                                                 INNER JOIN test.public.notify n on "user".id = n.id_user
                                    WHERE user_dialog = FALSE and ping_pm = TRUE and nickname= any($1::text[])''', msg)
            for item in record:
                if item[1] is None:
                    list_dinaid = (f'{list_dinaid}:cross_mark:[{item[1]}]'
                                   f'<a href="tg://user?id={item[0]}">{item[2]}</a>\n')
                else:
                    list_dinaid = f'{list_dinaid}:cross_mark:<a href="tg://user?id={item[0]}">{item[2]}</a>\n'
            await message.answer(emojize(f'{list_suck}\n\n{list_dinaid}'))
        else:
            record: Record = await pool.fetch('''SELECT test.public."user".id,guild,nickname from test.public."user"
                                                 WHERE nickname= any($1::text[])''', msg)
            list_send = ''
            for item in record:
                if item[1] is None:
                    list_send = f'{list_send}[{item[1]}]<a href="tg://user?id={item[0]}">{item[2]}</a>\n'
                else:
                    list_send = f'{list_send}<a href="tg://user?id={item[0]}">{item[2]}</a>\n'
            await message.answer(emojize(f'Ментнулись в ген. штаб!\n{list_send}'))
