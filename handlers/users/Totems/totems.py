from .totem_update import list_lvl_ge_de_ze, list_lvl_kronos, list_lvl_poseidon, list_lvl_ares, \
    list_nalog, list_aden, list_bronze, list_silver, list_gold
from aiogram import types
from loader import dp, db
from asyncpg import Connection, Record
from aiogram.utils.emoji import emojize
from utils.misc import rate_limit


@rate_limit(2, 'totems')
@dp.message_handler(commands='totems')
async def bot_command_get_totems(message: types.Message):
    pool: Connection = db
    temp_lst = [':dagger:Арес ', ':water_wave:Посейдон ', ':comet:Кронос ',
                ':flexed_biceps_medium-light_skin_tone:Гефест ',
                ':high_voltage:Зевс ', ':hourglass_not_done:Деймос ']
    temp_dict = {':dagger:Арес ': list_lvl_ares, ':water_wave:Посейдон ': list_lvl_poseidon,
                 ':comet:Кронос ': list_lvl_kronos,
                 ':flexed_biceps_medium-light_skin_tone:Гефест ': list_lvl_ge_de_ze,
                 ':high_voltage:Зевс ': list_lvl_ge_de_ze, ':hourglass_not_done:Деймос ': list_lvl_ge_de_ze}
    totems: Record = await pool.fetchrow('''SELECT * FROM test.public.totems 
                                            WHERE id_user = $1''', message.from_user.id,)
    if totems:
        all_bronze = 0
        all_silver = 0
        all_gold = 0
        all_aden = 0
        full_bronze = 0
        full_silver = 0
        full_gold = 0
        full_aden = 0
        total_nalog = [0, 0, 0, 0]
        user_nick: Record = await pool.fetchrow('''SELECT nickname FROM test.public."user" 
                                                WHERE id = $1''', message.from_user.id,)
        result = f'\nCводка по:moai:тотемам <a href="tg://user?id={message.from_user.id}">{emojize(user_nick[0])}</a>:'
        for item in temp_lst:
            if totems[temp_lst.index(item)*5+1] < 12:
                if totems[temp_lst.index(item)*5+1] == 0:
                    lvl_tot = 0
                else:
                    lvl_tot = temp_dict[item][totems[temp_lst.index(item)*5+1] - 1]
                aden_format = '{0:,}'.format(list_aden[totems[temp_lst.index(item)*5+1]]-totems[temp_lst.index(item)*5+2]).replace(',', ' ')
                result = (f'{result}\n<b>{item}</b>{totems[temp_lst.index(item)*5+1]}ур.(+{lvl_tot}%) -> '
                          f'{totems[temp_lst.index(item)*5+1]+1}ур.(+{temp_dict[item][totems[temp_lst.index(item)*5+1]]}%)'
                          f'\n:3rd_place_medal:{list_bronze[totems[temp_lst.index(item)*5+1]]-totems[temp_lst.index(item)*5+3]} '
                          f':2nd_place_medal:{list_silver[totems[temp_lst.index(item)*5+1]]-totems[temp_lst.index(item)*5+4]} '
                          f':1st_place_medal:{list_gold[totems[temp_lst.index(item)*5+1]]-totems[temp_lst.index(item)*5+5]}'
                          f' :rosette:{aden_format}\n')
                all_bronze += list_bronze[totems[temp_lst.index(item)*5+1]]-totems[temp_lst.index(item)*5+3]
                all_silver +=  list_silver[totems[temp_lst.index(item)*5+1]]-totems[temp_lst.index(item)*5+4]
                all_gold += list_gold[totems[temp_lst.index(item)*5+1]]-totems[temp_lst.index(item)*5+5]
                all_aden += list_aden[totems[temp_lst.index(item)*5+1]]-totems[temp_lst.index(item)*5+2]

                if temp_lst.index(item) >=0 and temp_lst.index(item) <3:
                    if totems[temp_lst.index(item)*5+1] == 11:
                        total_nalog[0] = total_nalog[0] + list_nalog[0][0][0]
                        total_nalog[1] = total_nalog[1] + list_nalog[0][1][0]
                        total_nalog[2] = total_nalog[2] + list_nalog[0][2][0]
                        total_nalog[3] = total_nalog[3] + list_nalog[0][3][0]
                    elif totems[temp_lst.index(item)*5+1] == 12:
                        total_nalog[0] = total_nalog[0] + list_nalog[0][0][1]
                        total_nalog[1] = total_nalog[1] + list_nalog[0][1][1]
                        total_nalog[2] = total_nalog[2] + list_nalog[0][2][1]
                        total_nalog[3] = total_nalog[3] + list_nalog[0][3][1]
                elif temp_lst.index(item) >2:
                    if totems[temp_lst.index(item)*5+1] == 11:
                        total_nalog[0] = total_nalog[0] + list_nalog[1][0][0]
                        total_nalog[1] = total_nalog[1] + list_nalog[1][1][0]
                        total_nalog[2] = total_nalog[2] + list_nalog[1][2][0]
                        total_nalog[3] = total_nalog[3] + list_nalog[1][3][0]
                    elif totems[temp_lst.index(item)*5+1] == 12:
                        total_nalog[0] = total_nalog[0] + list_nalog[1][0][1]
                        total_nalog[1] = total_nalog[1] + list_nalog[1][1][1]
                        total_nalog[2] = total_nalog[2] + list_nalog[1][2][1]
                        total_nalog[3] = total_nalog[3] + list_nalog[1][3][1]
                for item2 in list_bronze:
                    if item2 >= list_bronze[totems[temp_lst.index(item)*5+1]]:
                        full_bronze += item2
                full_bronze -= totems[temp_lst.index(item)*5+3]
                for item2 in list_silver:
                    if item2 >= list_silver[totems[temp_lst.index(item)*5+1]]:
                        full_silver += item2
                full_silver -= totems[temp_lst.index(item)*5+4]
                for item2 in list_gold:
                    if item2 >= list_gold[totems[temp_lst.index(item)*5+1]]:
                        full_gold += item2
                full_gold -= totems[temp_lst.index(item)*5+5]
                for item2 in list_aden:
                    if item2 >= list_aden[totems[temp_lst.index(item)*5+1]]:
                        full_aden += item2
                full_aden -= totems[temp_lst.index(item)*5+2]
            elif totems[temp_lst.index(item)*5+1] == 12:
                result = result + f'\n<b>{item}</b>максимального уровня:exclamation_mark:\n'

        procent_full_bronze_all = 0
        for item in list_bronze:
            procent_full_bronze_all += item*6
        procent_full_bronze = (procent_full_bronze_all-full_bronze) * 100 / procent_full_bronze_all / 4
        procent_full_silver_all = 0
        for item in list_silver:
            procent_full_silver_all += item*6
        procent_full_silver = (procent_full_silver_all-full_silver) * 100 / procent_full_silver_all / 4
        procent_full_gold_all = 0
        for item in list_gold:
            procent_full_gold_all += item*6
        procent_full_gold = (procent_full_gold_all-full_gold) * 100 / procent_full_gold_all / 4
        procent_full_aden_all = 0
        for item in list_aden:
            procent_full_aden_all += item*6
        procent_full_aden = (procent_full_aden_all-full_aden) * 100 / procent_full_aden_all / 4

        def toFixed(numObj, digits=2):
            return str(f"{numObj:.{digits}f}")

        procent_full = toFixed(procent_full_bronze + procent_full_silver + procent_full_gold + procent_full_aden)
        format_full_bronze = '{0:,}'.format(full_bronze).replace(',', ' ')
        format_full_silver = '{0:,}'.format(full_silver).replace(',', ' ')
        format_full_gold = '{0:,}'.format(full_gold).replace(',', ' ')
        format_full_aden = '{0:,}'.format(full_aden).replace(',', ' ')
        format_full = (f'\nВсего:({procent_full}%):3rd_place_medal:{format_full_bronze} :2nd_place_medal:'
                       f'{format_full_silver} :1st_place_medal:{format_full_gold} :rosette:{format_full_aden}')
        itog_aden_format = '{0:,}'.format(all_aden).replace(',', ' ')
        full_nalog = f'\n\n<b>Жертва богам в день:</b>\n' \
                     f'{total_nalog[0]}:3rd_place_medal: {total_nalog[1]}:2nd_place_medal: {total_nalog[2]}:1st_place_medal: {total_nalog[3]}:rosette:'
        itog = f'\nИтого: :3rd_place_medal:{all_bronze} :2nd_place_medal:{all_silver} :1st_place_medal:{all_gold} :rosette:{itog_aden_format}'

        await message.answer(emojize(f'{result}{itog}{format_full}{full_nalog}'))
        if message.from_user.id == message.chat.id:
            await message.delete()
        else:
            try:
                await message.delete()
            except:
                await message.answer('Не достаточно прав для удаления сообщения!')
    else:
        arg = message.from_user.id,0
        await pool.fetch('''INSERT INTO test.public.totems(id_user, atk, atk_a, atk_b, atk_s, atk_g, 
                                                               def, def_a, def_b, def_s, def_g, 
                                                               hp, hp_a, hp_b, hp_s, hp_g, 
                                                               dodge, dodge_a, dodge_b, dodge_s, dodge_g, 
                                                               crit, crit_a, crit_b, crit_s, crit_g, 
                                                               acc, acc_a, acc_b, acc_s, acc_g) 
                                values  ($1,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,
                                        $2,$2,$2,$2,$2,$2,$2,$2,$2,$2)''', *arg)
        await message.answer(f'Технические чебуреки!\n'
                             f'Используй команду /totems ещё раз')