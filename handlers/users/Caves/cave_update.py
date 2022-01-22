from aiogram import types
from loader import dp, db
from datetime import datetime, timedelta
from asyncpg import Connection
from aiogram.utils.emoji import demojize,emojize
from data.config import admins
from utils.misc import rate_limit
from aiogram.utils.exceptions import BotBlocked
from keyboards.inline.cave_cb_move import create_cb_cave_move


race_find = {':woman_astronaut:': 1, ':woman_elf:': 2, ':elf:‍:female_sign:': 2, ':robot:': 3}


@rate_limit(0, 'cave_update')
@dp.message_handler(user_id=admins, chat_type="private", commands='cave_update')
async def bot_command_rf_caves_update(message: types.Message):
    from asyncpg import Record
    pool: Connection = db
    msg = demojize(message.text).split(' ', maxsplit=1)[1]
    if msg.find(':mountain_cableway:Группа') != -1 or msg.find(':sled:Группа') != -1:
        if msg.find('поднимается на фуникулере в пещеры') != -1 or msg.find('поднимается на санях в пещеры') != -1:
            f_lead = ''
            for key in race_find:
                if msg.find(key) != -1:
                    f_race = key
                    zp_race = race_find[key]
                    f_lead = msg.split(key)[1].split(' поднимается')[0]
            if msg.find('пещеры') != -1:
                league = msg.split('пещеры(')[1].split(').')[0]
            elif msg.find('санях') != -1:
                league = msg.split('санях(')[1].split(').')[0]

            arg = f_lead.split(']', maxsplit=1)[1], f_lead.split(']', maxsplit=1)[0][1:], zp_race
            derg: Record = await pool.fetchrow('''SELECT lvl,id from test.public."user" 
                                                    WHERE nickname=$1 and guild=$2 and race=$3''', *arg)
            if not derg:
                arg = f_lead.split(']', maxsplit=1)[1], zp_race
                derg: Record = await pool.fetchrow('''SELECT lvl,id from test.public."user" 
                                                    WHERE nickname=$1 and race=$2''', *arg)

            records: Record = await pool.fetch('''SELECT test.public."user".id,guild,nickname,"user".lvl FROM test.public."user" 
                                                inner join test.public.notify n on "user".id = n.id_user
                                                WHERE user_dialog = TRUE and caves_update = TRUE and nickname
                                                in (select leader_n from test.public.caves where league=$1)''',
                                               league,)
            sd: Record = await pool.fetch('''select leader_n from test.public.caves where league=$1''', league,)
            arg = msg, f_lead, message.date, message.date-timedelta(minutes=10), f_race, league, f_lead.split(']',maxsplit=1)[0][1:],f_lead.split(']',maxsplit=1)[1], derg[0], derg[1], 0
            await pool.fetch('''INSERT INTO test.public.caves(text, leader, date_start, date_pvp, race, league,leader_g,leader_n,lvl,id_leader,room, start_move)
                                            values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$3)''', *arg)
            await message.delete()
            for item in records:
                try:
                    await message.bot.send_message(item[0], emojize(f':heavy_plus_sign::mountain_cableway:Поднялась новая группа:\n'
                                                                    f'<b>[{derg[0]}]{f_race}<a href="tg://user?id={derg[1]}">{f_lead}</a></b>\n'
                                                                    f'В вашей лиге <b>[{league}]</b> теперь -> <b>{len(sd)+1} групп</b>\n'
                                                                    f'Подробнее - /cave'), reply_markup=await create_cb_cave_move(item[0], message.date))
                except:
                    arg = False, item[0]
                    await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)
            bag_detect: Record = await pool.fetch('''SELECT id_leader,date_start from test.public.caves ''',)
            for bag in bag_detect:
                if datetime.now() - bag["date_start"] > timedelta(seconds=36000):
                    await pool.fetchval('''delete from test.public.caves WHERE id_leader=$1''', bag["id_leader"],)

            chat_cave: Record = await pool.fetchrow('''SELECT id_chat,id_message from test.public.cave_all_chat 
                                        where league=$1''', league,)
            if chat_cave:
                list_c_user =[]
                for user in await pool.fetch('''SELECT * from test.public.caves where league = $1 ORDER BY leader_g''', league,):
                    list_c_user.append(f'[{emojize(user["leader_g"])}]{emojize(user["leader_n"])} - {user["room"]}')
                await message.bot.edit_message_text(chat_id=chat_cave["id_chat"], text='\n\n'.join(list_c_user), message_id=chat_cave["id_message"])

        elif msg.find('спускается на фуникулере в ген. штаб') != -1 or msg.find('спускается на санях в ген. штаб') != -1:
            f_lead = ''
            for key in race_find:
                if msg.find(key) != -1:
                    f_race = key
                    f_lead = msg.split(key)[1].split(' спускается')[0]

            f_lvl = Record = await pool.fetchval('''SELECT lvl from test.public."user" WHERE nickname= $1''',
                                                 f_lead.split(']', maxsplit=1)[1],)
            if not f_lvl:
                f_lvl = 0
            await pool.fetchval('''delete from test.public.caves WHERE leader=$1''', f_lead)
            await message.delete()
            league = msg.split('пещер(')[1].split(').')[0]
            sd : Record = await pool.fetch('''select leader_n from test.public.caves where league=$1''', league,)
            record: Record = await pool.fetch('''SELECT test.public."user".id,guild,nickname,"user".lvl FROM test.public."user" 
                                                inner join test.public.notify n on "user".id = n.id_user
                                                WHERE user_dialog = TRUE and caves_update = TRUE and nickname
                                                in (select leader_n from test.public.caves where league=$1)''',
                                              league,)
            for item in record:
                try:
                    await message.bot.send_message(item[0], emojize(f':heavy_minus_sign::mountain_cableway:Из пещер вышла группа:\n'
                                                                    f'<b>[{f_lvl}]{f_race}{f_lead}</b>\n'
                                                                    f'В вашей лиге <b>[{league}]</b> теперь -> <b>{len(sd)} групп</b>\n'
                                                                    f'Подробнее - /cave'), reply_markup=await create_cb_cave_move(item[0], message.date))
                except:
                    arg = False, item[0]
                    await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)
            bag_detect: Record = await pool.fetch('''SELECT id_leader,date_start from test.public.caves ''',)
            for bag in bag_detect:
                if datetime.now() - bag["date_start"] > timedelta(seconds=36000):
                    await pool.fetchval('''delete from test.public.caves WHERE id_leader=$1''', bag["id_leader"],)
            chat_cave: Record = await pool.fetchrow('''SELECT id_chat,id_message from test.public.cave_all_chat 
                                        where league=$1''', league,)
            if chat_cave:
                list_c_user =[]
                for user in await pool.fetch('''SELECT * from test.public.caves where league = $1 ORDER BY leader_g''', league,):
                    list_c_user.append(f'[{emojize(user["leader_g"])}]{emojize(user["leader_n"])} - {user["room"]}')
                await message.bot.edit_message_text(chat_id=chat_cave["id_chat"], text='\n\n'.join(list_c_user), message_id=chat_cave["id_message"])
    elif msg.find(':trophy:Группа') != -1:
        msg = msg.split(':trophy:Группа ')[1]
        msg = msg.split(' победила группу ')
        msg[1] = msg[1].split(' в пещере')[0]
        for item in msg:
            for key in race_find:
                if item.find(key) != -1:
                    if msg.index(item) == 0:
                        arg = message.date, item.split(key)[1]
                        await pool.fetchval('''UPDATE test.public.caves 
                                                   SET date_pvp=$1, pvp_w = (select pvp_w+1 
                                                                             from test.public.caves 
                                                                             where leader = $2 limit 1) 
                                                   where leader = $2''', *arg)
                    elif msg.index(item) == 1:
                        arg = message.date, item.split(key)[1]
                        await pool.fetchval('''UPDATE test.public.caves 
                                                   SET date_pvp=$1, pvp_l = (select pvp_l+1 
                                                                             from test.public.caves 
                                                                             where leader = $2 LIMIT 1) 
                                                   where leader = $2''', *arg)

        await message.delete()
        bag_detect: Record = await pool.fetch('''SELECT id_leader,date_start from test.public.caves ''',)
        for bag in bag_detect:
            if datetime.now() - bag["date_start"] > timedelta(seconds=36000):
                await pool.fetchval('''delete from test.public.caves WHERE id_leader=$1''', bag["id_leader"],)
    elif msg.find(':handshake:Группы ') != -1:
        msg = msg.split(':handshake:Группы ')[1]
        msg = msg.split(' и ')
        msg[1] = msg[1].split(' сразились в р')[0]
        for item in msg:
            for key in race_find:
                if item.find(key) != -1:
                    arg = message.date, item.split(key)[1]
                    await pool.fetchval('''UPDATE test.public.caves 
                                               SET date_pvp=$1, pvp_n = (select pvp_n+1 
                                                                         from test.public.caves 
                                                                         where leader = $2 limit 1) 
                                               where leader = $2''', *arg)
        await message.delete()
        bag_detect: Record = await pool.fetch('''SELECT id_leader,date_start from test.public.caves ''',)
        for bag in bag_detect:
            if datetime.now() - bag["date_start"] > timedelta(seconds=36000):
                await pool.fetchval('''delete from test.public.caves WHERE id_leader=$1''', bag["id_leader"],)
