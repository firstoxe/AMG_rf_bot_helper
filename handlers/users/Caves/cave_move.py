from aiogram import types

from keyboards.inline.cave_room_cb import create_cb_cave_sel_room
from loader import dp, db
from asyncpg import Connection
from asyncpg import Record
from aiogram.utils.emoji import demojize, emojize
from utils.misc import rate_limit
from aiogram.utils.exceptions import MessageCantBeEdited, MessageNotModified
from filters.cave_move.cave_move import CaveMoveShag, CaveMoveShagComplite
from datetime import datetime, timedelta
from asyncio import sleep


@rate_limit(0, 'CaveMoveShag')
@dp.message_handler(CaveMoveShag())
async def cave_move_shag_start(message: types.Message):
    pool: Connection = db
    arg = message.forward_date, message.from_user.id
    usr: Record = await pool.fetchrow('''SELECT * from test.public.caves where id_leader= $1''', message.from_user.id)
    if (message.forward_date).timestamp() > (usr["start_move"].timestamp()):
        await pool.fetchval('''UPDATE test.public.caves SET start_move=$1 where id_leader = $2''', *arg)
        await message.answer(f'[{emojize(usr["leader_g"])}]{emojize(usr["leader_n"])} сделал 🏃🏻шаг, прибытие в след пещеру в {(message.forward_date+timedelta(seconds=30)).time()}',
                             reply_markup=await create_cb_cave_sel_room(message.from_user.id, message.date, '1-10'))
        await message.delete()


@rate_limit(0, 'CaveMoveShagComplite')
@dp.message_handler(CaveMoveShagComplite())
async def cave_move_shag_complite(message: types.Message):
    pool: Connection = db
    usr: Record = await pool.fetchrow('''SELECT * from test.public.caves where id_leader= $1''', message.from_user.id)
    if (message.forward_date).timestamp() > (usr["start_move"]).timestamp():
        room = int(message.text[-2:].replace('№', '').strip())
        arg = room, message.from_user.id
        await pool.fetchval('''UPDATE test.public.caves SET room=$1 where id_leader = $2''', *arg)
        if message.forward_date+timedelta(seconds=90) >= datetime.now():
            await message.answer(f'[{emojize(usr["leader_g"])}]{emojize(usr["leader_n"])} прибыл в 🚠пещеру №<b>{room}</b>\n'
                                 f'КД до {(message.forward_date+timedelta(seconds=90)).time()} ≈ '
                                 f'{((message.forward_date+timedelta(seconds=90))-datetime.now()).seconds} сек')
        else:
            await message.answer(f'[{emojize(usr["leader_g"])}]{emojize(usr["leader_n"])} прибыл в 🚠пещеру №<b>{room}</b>\n'
                                 f'КД прошло')
        await message.delete()

        usr_pin: Record = await pool.fetch('''SELECT * from test.public.caves 
                                      where league = (select league from test.public.caves where id_leader = $1)
                                      ORDER BY leader_g, room''', message.from_user.id,)
        chat_pin: Record = await pool.fetchrow('''SELECT id_chat,id_message from test.public.cave_all_chat 
                                        where league=(select league from test.public.caves where id_leader=$1)''',
                                               message.from_user.id,)
        list_user_pin = []

        try:
            if chat_pin[0] == message.chat.id:
                for user in usr_pin:
                    list_user_pin.append(f'[{emojize(user["leader_g"])}]{emojize(user["leader_n"])} - {user["room"]}')

            await message.bot.edit_message_text(text='\n\n'.join(list_user_pin),chat_id=message.chat.id, message_id=chat_pin[1])
        except MessageNotModified:
            pass
        except Exception as e:
            pass


        arg = usr["leader_g"], room, usr["league"], usr["id_leader"]
        all_run: Record = await pool.fetch("""SELECT * 
        from test.public.caves 
        where leader_g != $1 and room =$2 and league=$3 
            and date_pvp+ interval '8 minute' < now()+ interval '3 hour'
            and (select date_pvp from caves where id_leader=$4) + interval '8 minute' < now()+ interval '3 hour'""", *arg)
        list_run = []
        if all_run:
            for item in all_run:
                list_run.append(f'🏃🏻 RUN!!! [{emojize(item["leader_g"])}]<a href="tg://user?id={item["id_leader"]}">{emojize(item["leader_n"])}</a>')
        if list_run:
            chat_id: Record = await pool.fetchrow('''SELECT id_chat from test.public.cave_all_chat where league=$1''', usr["league"],)
            await message.bot.send_message(chat_id=chat_id["id_chat"],text='\n'.join(list_run))
            await sleep(1)
            await message.bot.send_message(chat_id=chat_id["id_chat"],text='\n'.join(list_run))
            await sleep(1)
            await message.bot.send_message(chat_id=chat_id["id_chat"],text='\n'.join(list_run))


