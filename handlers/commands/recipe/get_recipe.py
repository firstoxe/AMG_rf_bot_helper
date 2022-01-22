from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import RegexpCommandsFilter
from aiogram.utils.emoji import emojize
from aiogram.utils import emoji
from utils.misc import rate_limit
from asyncpg import Connection, Record
from loader import db
from filters.work_with_user import helper_user

@rate_limit(2, 'get_recipe')
@dp.message_handler(commands=['get_recipe'])
async def bot_get_recipe(message: types.Message):
    pool: Connection = db
    record: Record = await pool.fetch('SELECT * FROM test.public.recipes where name=$1 or name_a = $1 or name_b = $1',(message.text.split(' ',maxsplit=1)[1]).lower())
    result = ''
    if not record:
        await message.answer(f'{await helper_user(message.from_user.id)} \nНазвание рецепта указано неверно!\n'
                             f'Если не помнишь правильное название используй команду /get_recipe_lvl 55\n'
                             f'Где 55 - это урвень предмета')
    else:
        if record[0][1] != None:
                result = result + ':red_heart: +' + str(record[0][1]) + '\n'
        if record[0][2] != None:
                result = result + ':crossed_swords: +' + str(record[0][2]) + '\n'
        if record[0][3] != None:
                result = result + ':shield: +' + str(record[0][3]) + '\n'
        if record[0][4] != None:
                result = result + ':dashing_away: +' + str(record[0][4]) + '\n'
        if record[0][5] != None:
                result = result + ':direct_hit: +' + str(record[0][5]) + '\n'
        if record[0][6] != None:
                result = result + ':crystal_ball: +' + str(record[0][6]) + '\n'
        if record[0][7] != None:
                result = result + ':hourglass_not_done: +' + str(record[0][7]) + '\n'
        await message.answer(emoji.emojize(f'{await helper_user(message.from_user.id)} держи: \nМаксимальные статы для <b>{record[0][0]}</b>\n{result}'))



@dp.message_handler(RegexpCommandsFilter(regexp_commands=['get_recipe_lvl_([0-9]*)']))
async def bot_get_recipe_lvl(message: types.Message, regexp_command):
    pool: Connection = db
    user_nick: Record = await pool.fetchrow('''SELECT nickname FROM test.public."user" 
                                                WHERE id = $1''', message.from_user.id,)
    record: Record = await pool.fetch('SELECT name FROM test.public.recipes where lvl=$1 or name_a = $1 or name_b = $1',(message.text.split(' ',maxsplit=1)[1]).lower())
    
    await message.reply(f"You have requested an item with id <code>{regexp_command.group(1)}</code>")