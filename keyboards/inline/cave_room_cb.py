from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageCantBeEdited, MessageNotModified
from asyncpg import Connection, Record
from asyncio import sleep
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime,timedelta


dat_cave_room = CallbackData('cave_move', 'action', 'id', 'date', 'room')

async def create_cb_cave_sel_room(id, date, diapason):
    kb = InlineKeyboardMarkup(row_width=3)
    diapason_start = int(diapason.split('-')[0])
    diapason_end = int(diapason.split('-')[1])
    ch = 1
    list_kb = []
    while diapason_start <= diapason_end:
        if ch != 4 and ch <= diapason_end:
            list_kb.append(InlineKeyboardButton(str(diapason_start), callback_data=dat_cave_room.new('caveSelRoom',str(id),str(date).replace(':',';'),str(diapason_start))))
            ch += 1
            diapason_start += 1
        else:
            kb.add(*list_kb)
            list_kb = []
            ch = 1
    if len(list_kb)>0:
        kb.add(*list_kb)
    return kb



@dp.callback_query_handler(dat_cave_room.filter(action=['caveSelRoom']))
async def inline_kb_mob_loc_back1(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        pool: Connection = db
        usr: Record = await pool.fetchrow('''SELECT * from test.public.caves where id_leader= $1''', int(callback_data["id"]),)
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            if usr["start_move"]+timedelta(seconds=120) >= datetime.now():
                text_anws = (f'[{emojize(usr["leader_g"])}]{emojize(usr["leader_n"])} прибыл в 🚠пещеру №<b>{callback_data["room"]}</b>\n'
                             f'КД до {(usr["start_move"]+timedelta(seconds=120)).time()} <b>-></b> {((usr["start_move"]+timedelta(seconds=120))-datetime.now()).seconds} сек')
            else:
                text_anws = (f'[{emojize(usr["leader_g"])}]{emojize(usr["leader_n"])} прибыл в 🚠пещеру №<b>{callback_data["room"]}</b>\n'
                             f'КД прошло')
            await query.bot.edit_message_text(text=text_anws,
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id)
            room = int(callback_data["room"])
            arg = room, int(callback_data["id"])
            await pool.fetchval('''UPDATE test.public.caves SET room=$1 where id_leader = $2''', *arg)
            usr_pin: Record = await pool.fetch('''SELECT * from test.public.caves 
                                          where league = (select league from test.public.caves where id_leader = $1)
                                          ORDER BY leader_g, room''', int(callback_data["id"]),)
            chat_pin: Record = await pool.fetchrow('''SELECT id_chat,id_message from test.public.cave_all_chat 
                                            where league=(select league from test.public.caves where id_leader=$1)''',
                                                   int(callback_data["id"]),)
            list_user_pin = []

            try:
                if chat_pin[0] == query.message.chat.id:
                    for user in usr_pin:
                        list_user_pin.append(f'[{emojize(user["leader_g"])}]{emojize(user["leader_n"])} - {user["room"]}')

                await query.message.bot.edit_message_text(text='\n\n'.join(list_user_pin),chat_id=query.message.chat.id, message_id=chat_pin[1])
            except MessageNotModified:
                pass
            except Exception as e:
                print('Пизда')

            arg = usr["leader_g"], room, usr["league"], usr["id_leader"]
            all_run: Record =await pool.fetch("""SELECT * from test.public.caves  
            where leader_g != $1 and room =$2 
                and league=$3 and date_pvp+ interval '8 minute' < now()+ interval '3 hour'
                and (select date_pvp from caves where id_leader=$4) + interval '8 minute' < now()+ interval '3 hour'""",*arg)
            list_run = []
            if all_run:
                for item in all_run:
                    list_run.append(f'🏃🏻 RUN!!! [{emojize(item["leader_g"])}]<a href="tg://user?id={item["id_leader"]}">{emojize(item["leader_n"])}</a>')
            if list_run:
                chat_id: Record = await pool.fetchrow('''SELECT id_chat from test.public.cave_all_chat where league=$1''', usr["league"],)
                await query.message.bot.send_message(chat_id=chat_id["id_chat"],text='\n'.join(list_run))
                await sleep(1)
                await query.message.bot.send_message(chat_id=chat_id["id_chat"],text='\n'.join(list_run))
                await sleep(1)
                await query.message.bot.send_message(chat_id=chat_id["id_chat"],text='\n'.join(list_run))
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=7200)
            await query.message.edit_text(':cross_mark:Прошло больше часа!!\n'
                                          'Можно было и побыстрее =)')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=7200)