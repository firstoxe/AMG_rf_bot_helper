from aiogram import types
from loader import dp
from filters.all_item_check.auc_item import AucItemCheck
from aiogram.utils.emoji import emojize, demojize
from utils.misc import rate_limit
from asyncpg import Connection, Record
from loader import db
from filters.work_with_user import helper_user


@rate_limit(1, 'auc_item_check')
@dp.message_handler(AucItemCheck())
async def bot_auc_item_ch(message: types.Message):
    pool: Connection = db
    list_item =[]
    list_item.append(f'{await helper_user(message.from_user.id)} держи:\n')
    for item in message.text.splitlines():
        msg = demojize(item.text).split(' ', maxsplit=1)[1]
        item_stat = msg.split(' ')
        if item_stat[0].find(')') != -1:
            item_stat.remove(item_stat[0])
        name_rec = item_stat[0]
        if item_stat[1].find('(') != -1:
            name_rec = name_rec + ' ' + item_stat[1].split('(')[0]
        else:
            name_rec = name_rec + ' ' + item_stat[1]

        record: Record = await pool.fetchrow('SELECT * FROM test.public.recipes '
                                             'where name=$1 or name_a = $1 or name_b = $1', name_rec.lower())


        list_item.append(f'{await stat_for_item(item_stat,record,name_rec)}\n')
        await message.answer('\n'.join(list_item))
    else:
        await message.answer(emojize('Пример использования команды:\n/item Меч Равновесия :crossed_swords:799.7 '
                                     ':direct_hit:+0.95% :red_heart:95 :sports_medal:50 '
                                     ':crystal_ball:+2.45% :biohazard: +4'))





async def stat_for_item(item_stat,record,name_rec):
    i_atk = 0
    i_def = 0
    i_crit = 0
    i_dodge = 0
    i_hp = 0
    i_acc = 0
    i_exp = 0

    for item in item_stat:
        if item.find(':crossed_swords:') != -1:
            i_atk = float(item.split(':crossed_swords:')[1])
        if item.find(':direct_hit:') != -1:
            i_crit = float(item.split(':direct_hit:')[1][1:-1])
        if item.find(':red_heart:') != -1:
            i_hp = int(item.split(':red_heart:')[1])
        if item.find(':crystal_ball:') != -1:
            i_exp = float(item.split(':crystal_ball:')[1][1:-1])
        if item.find(':shield:') != -1:
            i_def = float(item.split(':shield:')[1])
        if item.find(':hourglass_not_done:') != -1:
            i_acc = float(item.split(':hourglass_not_done:')[1][1:-1])
        if item.find(':dashing_away:') != -1:
            i_dodge = float(item.split(':dashing_away:')[1][1:-1])
    talik = 0
    talik2 = ''
    for item in item_stat:
        if item.find(':biohazard:') != -1:
            talik = int(item_stat[item_stat.index(item)+1][1:])
            ls_talik = [0, 2, 4, 7, 10, 13, 18, 25]
            i_atk = i_atk-i_atk/(100+ls_talik[talik])*ls_talik[talik]
            talik2 = ':biohazard:'
        if item.find(':blue_circle:') != -1:
            talik = int(item_stat[item_stat.index(item)+1][1:])
            ls_talik = [0, 3, 6, 11, 16, 21, 28, 40]
            i_def = i_def-i_def/(100+ls_talik[talik])*ls_talik[talik]
        if item.find(':red_circle:') != -1:
            talik = int(item_stat[item_stat.index(item)+1][1:])
            ls_talik = [0, 1, 2, 4, 6, 8, 12, 18]
            i_crit = i_crit-ls_talik[talik]
            talik2 = ':red_circle:'
        if item.find(':black_circle:') != -1:
            talik = int(item_stat[item_stat.index(item)+1][1:])
            ls_talik = [0, 1, 2, 4, 6, 8, 12, 18]
            i_dodge = i_dodge-ls_talik[talik]
            talik2 = ':black_circle:'

    result = ''
    if record:
        if record[1] is not None:
            result = f'{result}:red_heart: {i_hp}[<b>{int(i_hp)-record[1]}</b>]  '
        if record[2] is not None:
            result = f'{result}:crossed_swords: {i_atk:.{0}f}[<b>{i_atk-record[2]:.{0}f}</b>]  '
        if record[3] is not None:
            result = f'{result}:shield: {i_def:.{0}f}[<b>{i_def-record[3]:.{0}f}</b>]  '
        result= f'{result}\n'
        if record[4] is not None:
            result = f'{result}:dashing_away: {i_dodge}%[<b>{i_dodge-record[4]:.{2}f}</b>]  '
        if record[5] is not None:
            result = f'{result}:direct_hit: {i_crit}%[<b>{i_crit-record[5]:.{2}f}</b>]  '
        if record[7] is not None:
            result = f'{result}:hourglass_not_done: {i_acc}%[<b>{i_acc-record[7]:.{2}f}</b>]  '
        result= f'{result}\n'
        if record[6] is not None:
            result = f'{result}:crystal_ball: {i_exp}%[<b>{i_exp-record[6]:.{2}f}</b>]  '
        return emojize(f'\n<b>{name_rec}</b> +{talik}{talik2}\n\n{result}')

