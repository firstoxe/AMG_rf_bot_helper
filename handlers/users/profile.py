from datetime import datetime, timedelta

from aiogram import types
from aiogram.utils.emoji import demojize, emojize
from asyncpg import Connection, Record

from loader import dp, db
from .Totems.totem_update import list_lvl_ge_de_ze, list_lvl_kronos, list_lvl_poseidon, list_lvl_ares

from filters.profile_filter import profileUpdate
from filters.guild_check import check_g
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def tot(tott, lvl_totems):
    if lvl_totems.get(tott) is not None:
        if tott == 'atk':
            return list_lvl_ares.index(float(lvl_totems.get(tott)))+1
        elif tott == 'defense':
            return list_lvl_poseidon.index(float(lvl_totems.get(tott)))+1
        elif tott == 'hp':
            return list_lvl_kronos.index(int(lvl_totems.get(tott)))+1
        else:
            return list_lvl_ge_de_ze.index(float(lvl_totems.get(tott)))+1
    else:
        return 0


def for_stat(new,original,type_return):

    if float(new) != float(original):
        if float(new) > float(original):
            return f'+{toFixed(float(new)-float(original), type_return)}'
        elif float(new) < float(original):
            return f'{toFixed(float(new)-float(original), type_return)}'
    elif float(new) == float(original):
        return f'{toFixed(float(new)-float(original), type_return)}'


def get_paragon(exp=0):
    paragon_exp = int(exp) - 14200000
    ch_w = 0
    paragon_exp3 = 0
    while paragon_exp > paragon_exp3:
        if ch_w < 26:
            paragon_exp3 += 75000
        elif ch_w > 25 and ch_w < 51:
            paragon_exp3 += 80000
        elif ch_w > 50 and ch_w < 76:
            paragon_exp3 += 85000
        elif ch_w > 75 and ch_w < 101:
            paragon_exp3 += 95000
        elif ch_w > 100 and ch_w < 126:
            paragon_exp3 += 100000
        elif ch_w > 125 and ch_w < 151:
            paragon_exp3 += 105000
        elif ch_w > 150 and ch_w < 201:
            paragon_exp3 += 110000
        elif ch_w > 200 and ch_w < 251:
            paragon_exp3 += 120000
        elif ch_w > 250 and ch_w < 301:
            paragon_exp3 += 130000
        elif ch_w > 300 and ch_w < 351:
            paragon_exp3 += 140000
        elif ch_w > 350 and ch_w < 401:
            paragon_exp3 += 160000
        elif ch_w > 400 and ch_w < 451:
            paragon_exp3 += 180000
        elif ch_w > 450 and ch_w < 501:
            paragon_exp3 += 200000
        elif ch_w > 500 and ch_w < 551:
            paragon_exp3 += 225000
        elif ch_w > 550 and ch_w < 601:
            paragon_exp3 += 250000
        elif ch_w > 600 and ch_w < 651:
            paragon_exp3 += 275000
        elif ch_w > 650 and ch_w < 701:
            paragon_exp3 += 300000
        elif ch_w > 700 and ch_w < 751:
            paragon_exp3 += 325000
        elif ch_w > 750 and ch_w < 801:
            paragon_exp3 += 350000
        elif ch_w > 800 and ch_w < 851:
            paragon_exp3 += 375000
        elif ch_w > 850 and ch_w < 901:
            paragon_exp3 += 400000
        elif ch_w > 900:
            paragon_exp3 += 425000
        ch_w += 1

    return '{0:,}'.format(paragon_exp3-paragon_exp).replace(',', ' ')


race_find = {':woman_astronaut:': 1,':woman_elf:': 2, ':elf:‍:female_sign:': 2, ':robot:': 3}

race_find2 = {'Basilaris': 1, 'Castitas': 2, 'Aquilla': 3}


lvl_list = [0, 200, 625, 1125, 1750, 2500, 3375, 4375, 5500, 6750,
            8125, 9625, 11250, 13000, 17850, 20250, 22800, 25500, 28350, 31350,
            34500, 37800, 41250, 44850, 48600, 52500, 56550, 62400, 66750, 71250,
            80250, 120500, 170000, 220500, 310000, 410000, 530000, 670000, 830000, 980000,
            1160000, 1320000, 1550000, 1900000, 2450000, 3300000, 4400000, 6000000, 8100000, 14200000,
            27700000, 38200000, 50500000, 65300000, 80000000]
lvl_kopatel = [0, 6048, 12096, 24192, 48384, 72576, 101010, 157680, 214548, 372624]
lvl_eter = [0, 800, 3080, 11000, 26400, 54000, 96000, 176000, 254000, 350000]



@dp.message_handler(profileUpdate())
async def bot_forward_profile(message: types.Message):
    if(datetime.now() - message.forward_date).seconds <= 600:
        arg = message.from_user.id

        abu_mess = True
        msg = demojize(message.text).splitlines()
        id_user = 0
        race = 0
        guild = None
        nickname = None
        hp = 0
        lvl = 0
        paragon = 0
        pvp = 0
        kopka = 0
        eter = 0
        atk = 0
        defense = 0
        dodge = 0
        critical = 0
        accuracy = 0
        exp_bonus = 0
        lvl_totems = {}
        prem = None
        prem_abu = None
        exp = 0
        aden = 0
        diamond = 0
        cred = 0
        pm = False
        prof_bel = 1
        prof_cor = 1
        prof_acr = 1
        buff_lamp = '123'
        if message.from_user.username is not None:
            username = message.from_user.username
        else:
            username = 'NULL'
        for item in msg:
            if item.find('Раса: :') != -1:
                for key in race_find2:
                    if item.find(key) != -1:
                        race = race_find2[key]
            if item.find('Ник: ') != -1:
                nickname = item.split('Ник: ')[1]
                if nickname.find(']') > 1 and nickname.find(']') != len(nickname)-1:
                    guild = nickname.split(']', maxsplit=1)[0][1:]
                    nickname = nickname.split(']', maxsplit=1)[1]
            if item.find('Идентификатор: ') != -1:
                id_user = int(item.split('Идентификатор: ')[1])
                pool: Connection = db
                record: Record = await pool.fetchrow('''SELECT * FROM test.public.user WHERE id = $1''', arg,)
            if item.find(':red_heart:Здоровье: ') != -1:
                hp = int(item.split('/')[1])
            if item.find(':sports_medal:Уровень: ') != -1:
                if item.find('/paragon') != -1:
                    lvl = int(item.split('Уровень: ')[1].split('(')[0])
                    paragon = int(item.split('(')[1].split(')')[0])
                else:
                    lvl = int(item.split('Уровень: ')[1])
            if item.find(':oncoming_fist_light_skin_tone:PVP: ') != -1:
                pvp = int(item.split('PVP: ')[1].replace(' ', ''))
            if item.find(':pick:Копатель: ') != -1:
                kopka = int(item.split(':full_moon:')[1].split('/')[0].replace(' ', ''))
            if item.find(':flashlight:Добытчик: ') != -1:
                eter = int(item.split(':full_moon:')[1].split('/')[0].replace(' ', ''))
            if item.find(':crossed_swords:Атака: ') != -1 and item.find(':shield:Защита: ') != -1:
                tmp = item.split(':crossed_swords:Атака: ')[1].split(')')[0]
                atk = int(tmp.split(' (+')[1])+int(tmp.split(' (+')[0])
                tmp = item.split(':shield:Защита: ')[1].split(')')[0]
                defense = int(tmp.split(' (+')[1])+int(tmp.split(' (+')[0])
            if item.find(':dashing_away:Уворот: ') != -1 and item.find(':bullseye:Крит: ') != -1:
                tmp = item.split(':dashing_away:Уворот: ')[1].split('%)')[0]
                dodge = float(tmp.split('% (+')[1])+float(tmp.split('% (+')[0])
                tmp = item.split(':bullseye:Крит: ')[1].split('%)')[0]
                critical = float(tmp.split('% (+')[1])+float(tmp.split('% (+')[0])
                critical = float(f"{critical:.2f}")
            if item.find(':hourglass_not_done:Точность: ') != -1:
                accuracy = float(item.split(':hourglass_not_done:Точность: ')[1].split('% (+')[0]) + \
                           float(item.split('% (+')[1].split('%)')[0])
            if item.find(':crystal_ball:Доп. опыт: ') != -1 and item.find(':rosette:Доп. аден: ') != -1:
                exp_bonus = float(item.split(':crystal_ball:Доп. опыт: ')[1].split('% :rosette:')[0])

            if item.find(':dagger:Ареса: :crossed_swords:+') != -1:
                lvl_totems.update({'atk': item.split(':crossed_swords:+')[1].split('%')[0]})
            if item.find(':water_wave:Посейдона: :shield:+') != -1:
                lvl_totems.update({'defense': item.split(':shield:+')[1].split('%')[0]})
            if item.find(':flexed_biceps_medium-light_skin_tone:Гефеста: :dashing_away:+') != -1:
                lvl_totems.update({'dodge': item.split(':dashing_away:+')[1].split('%')[0]})
            if item.find(':high_voltage:Зевса: :bullseye:+') != -1:
                lvl_totems.update({'critical': item.split(':bullseye:+')[1].split('%')[0]})
            if item.find(':comet:Кроноса: :red_heart:+') != -1:
                lvl_totems.update({'hp': item.split(':red_hea rt:+')[1].split('%')[0]})
            if item.find(':hourglass_not_done:Деймоса: :hourglass_not_done:+') != -1:
                lvl_totems.update({'acc': item.split(':hourglass_not_done:+')[1].split('%')[0]})
            if item.find(':reminder_ribbon:Премиум аккаунт по - ') != -1:
                prem = datetime.strptime(item.split(':reminder_ribbon:Премиум аккаунт по - ')[1], '%d.%m.%Y').date()
            if item.find(':trackball:АБУ - ') != -1:
                if item.find('(копает)') != -1:
                    prem_abu = datetime.strptime(item.split(':trackball:АБУ - ')[1].split(' (копает)')[0], '%d.%m.%Y').date()
                    abu_mess = False
                else:
                    prem_abu = datetime.strptime(item.split(':trackball:АБУ - ')[1].replace(' ', ''), '%d.%m.%Y').date()
                    abu_mess = True

            if item.find(':full_moon:Опыт: ') != -1:
                exp = float(item.split(':full_moon:Опыт: ')[1].split('/')[0].replace(' ', ''))
                if not prem_abu:
                    abu_mess = False
            if item.find(':rosette:Аден: ') != -1:
                aden = int(item.split(':rosette:Аден: ')[1].replace(' ', ''))
            if item.find(':money_bag:Кредитов: ') != -1:
                cred = int(item.split(':money_bag:Кредитов: ')[1].replace(' ', ''))
            if item.find(':gem_stone:Алмазов: ') != -1:
                diamond = int(item.split(':gem_stone:Алмазов: ')[1].replace(' ', ''))
            if message.chat.id == message.from_user.id:
                pm = True
            else:
                pm = False

            if item.find(':man_scientist:Кибернетик: ') != -1:
                prof_bel = int(item.split(':man_scientist:Кибернетик: ')[1].split('(')[0])
            if item.find(':man_mage:Жрец: ') != -1:
                prof_cor = int(item.split(':man_mage:Жрец: ')[1].split('(')[0])
            if item.find(':man_in_suit_levitating:Аннигилятор: ') != -1:
                prof_acr = int(item.split(':man_in_suit_levitating:Аннигилятор: ')[1].split('(')[0])
        if not record:
            if prem == 'NULL':
                prem = message.date-timedelta(days=100)
            if prem_abu == 'NULL':
                prem_abu = message.date-timedelta(days=100)
            arg = id_user, username, race,guild, nickname, lvl, paragon, hp, atk, defense, dodge, critical, accuracy,\
                  exp, exp_bonus, prem, prem_abu, message.forward_date, aden, diamond, pvp, cred, eter, kopka, pm,prof_bel,prof_cor,prof_acr

            await pool.fetch('''INSERT INTO test.public.user(id, username, race, guild, nickname, lvl, 
                                                     paragon, hp, atk, def, dodge, crit, accuracy, exp, exp_bonus, 
                                                     premium, abu, date_update, aden, diamond, pvp, credits, exp_earner, 
                                                     exp_digger, user_dialog, last_activity,lvl_prof_bel,lvl_prof_cor,
                                                     lvl_prof_acr) values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,
                                                     $14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$17,$26,$27,$28)''',
                                                      *arg)


            arg = message.from_user.id,tot("atk",lvl_totems),0,0,0,0,tot("defense",lvl_totems),0,0,0,0,\
                  tot("hp",lvl_totems),0,0,0,0,tot("dodge",lvl_totems),0,0,0,0,tot("critical",lvl_totems),\
                  0,0,0,0,tot("acc",lvl_totems),0,0,0,0
            await pool.fetch('''INSERT INTO test.public.totems(id_user, atk, atk_a, atk_b, atk_s, atk_g, 
                                                               def, def_a, def_b, def_s, def_g, 
                                                               hp, hp_a, hp_b, hp_s, hp_g, 
                                                               dodge, dodge_a, dodge_b, dodge_s, dodge_g, 
                                                               crit, crit_a, crit_b, crit_s, crit_g, 
                                                               acc, acc_a, acc_b, acc_s, acc_g) 
                                values  ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12, $13,$14,$15,$16,$17,$18,$19,$20,$21,
                                        $22,$23,$24,$25,$26,$27,$28,$29,$30,$31)''', *arg)

            arg = [message.from_user.id]
            await pool.fetch('''INSERT INTO test.public.notify(id_user) values ($1)''', *arg)
            await pool.fetch('''INSERT INTO test.public.top_conf(id_user) values ($1)''', *arg)

            await message.answer(emojize(f'@{username} Профиль создан!\n{race}\n[{guild}]{nickname}\n{id_user}\n:sports_medal:{lvl}({paragon})\n'
                                         f':red_heart:{hp}\n:oncoming_fist_light_skin_tone:{pvp}\n'
                                         f':pick:{kopka} :flashlight:{eter}\n'
                                         f':crossed_swords:{atk} :shield:{defense}\n'
                                         f':dashing_away:{dodge} :direct_hit:{critical} :hourglass_not_done:{accuracy}'
                                         f':crystal_ball:{exp_bonus}%\n\n'
                                         f'Тотемы:\n'
                                         f':dagger:{lvl_totems.get("atk")}:water_wave:{lvl_totems.get("defense")}:high_voltage:{lvl_totems.get("critical")}'
                                         f':flexed_biceps_medium-light_skin_tone:{lvl_totems.get("dodge")}:comet:{lvl_totems.get("hp")}'
                                         f':hourglass_not_done:{lvl_totems.get("acc")}\n'
                                         f':reminder_ribbon:{prem}:trackball:{prem_abu}\n'
                                         f':full_moon:{exp}:rosette:{aden}:money_bag:{cred}:gem_stone:{diamond}'))
            #await pool.close()
            await message.delete()
        else:

            diff = datetime.now() - record[17]
            days, seconds = diff.days, diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60


            anws = (f'{check_g(guild)}<a href="tg://user?id={message.from_user.id}">{emojize(nickname)}</a>\n'
                    f'C последнего обновления прошло :hourglass_not_done:{days}д. {hours}ч. {minutes}м. {seconds}с.\n\n'
                    f'<b>Изменения по статам</b>:\n'
                    f':red_heart:{for_stat(hp,record[7],0)} :crossed_swords:{for_stat(atk,record[8],0)} :shield:{for_stat(defense,record[9],0)}\n'
                    f' :dashing_away:{for_stat(dodge,record[10],2)} :direct_hit:{for_stat(critical,record[11],2)} :hourglass_not_done:{for_stat(accuracy,record[12],2)}')


            anws = (f'{anws}\n\n<b>Тотемы</b>:\n'
                    f':dagger:{tot("atk",lvl_totems)} :water_wave:{tot("defense",lvl_totems)} :comet:{tot("hp",lvl_totems)} '
                    f':flexed_biceps_medium-light_skin_tone:{tot("dodge",lvl_totems)} :hourglass_not_done:{tot("acc",lvl_totems)} :high_voltage:{tot("critical",lvl_totems)} - /totems')

            if for_stat(kopka,record[23], 0) != 0:
                for item in lvl_kopatel:
                    if item >= kopka:

                        break
            else:
                item = 0

            if for_stat(eter, record[22], 0) != 0:
                for item2 in lvl_eter:
                    if item2 >= eter:

                        break
            else:
                item2 = 0

            try:
                if hours > 0 or days > 0:
                    days, seconds = diff.days, diff.seconds
                    hours = days * 24 + seconds // 3600

                    if int(kopka) != int(record[23]):
                        speed = (kopka-record[23])//hours
                        speed_d = int((item-kopka) // speed // 24)
                        speed_h = int((item-kopka) // speed -speed_d*24)
                        anws = f'{anws}\n\n:pick:{item-kopka}:full_moon: до {lvl_kopatel.index(item)+1}:sports_medal:ур. ≈ {speed_d}д. {speed_h}ч.'
                    else:
                        anws = f'{anws}\n\n:pick:{item-kopka}:full_moon: до {lvl_kopatel.index(item)+1}:sports_medal:ур. ≈ ∞'
                    if int(eter) != int(record[22]):
                        speed = (eter-record[22])//hours
                        speed_d = int((item2-eter) // speed // 24)
                        speed_h = int((item2-eter) // speed - speed_d*24)
                        anws = f'{anws}\n:flashlight:{item2-eter}:full_moon: до {lvl_eter.index(item2)+1}:sports_medal:ур. ≈ {speed_d}д. {speed_h}ч.'
                    else:
                        anws = f'{anws}\n:flashlight:{item2-eter}:full_moon: до {lvl_eter.index(item2)+1}:sports_medal:ур. ≈ ∞'
                else:
                    anws = f'{anws}\n\n:pick:{item-kopka}:full_moon: до {lvl_kopatel.index(item)+1}:sports_medal:ур. ≈ ∞'
                    anws = f'{anws}\n:flashlight:{item2-eter}:full_moon: до {lvl_eter.index(item2)+1}:sports_medal:ур. ≈ ∞'
            except:
                anws = f'{anws}\n\n:pick:{item-kopka}:full_moon: до {lvl_kopatel.index(item)+1}:sports_medal:ур. ≈ ∞'
                anws = f'{anws}\n:flashlight:{item2-eter}:full_moon: до {lvl_eter.index(item2)+1}:sports_medal:ур. ≈ ∞'

            hours = days * 24 + seconds // 3600
            for item in lvl_list:
                if item >= exp:
                    break

            format_exp = '{0:,}'.format(int(toFixed(item - exp, 0))).replace(',', ' ')
            try:
                if exp - record[13] > 0:
                    if hours > 0:
                        p_exp = int((exp - record[13]) // hours)
                        speed_d = int((item-exp) // p_exp // 24)
                        speed_h = int((item-exp) // p_exp -speed_d * 24)
                        anws = (f'{anws}\n\nПолучено опыта:full_moon:{for_stat(exp,record[13],0)} ≈ {p_exp} опыта в час\n'
                                f':full_moon:{format_exp} до {lvl_list.index(item)+1}:sports_medal:ур. ≈ {speed_d}д. {speed_h}ч.')
                    else:
                        anws = (f'{anws}\n\nПолучено опыта:full_moon:{for_stat(exp,record[13],0)} ≈ '
                                f':full_moon:{format_exp} до {lvl_list.index(item)+1}:sports_medal:ур.')
                else:
                    anws = (f'{anws}\n\n:full_moon:{format_exp} до {lvl_list.index(item)+1}:sports_medal:ур. ≈ ∞')
            except:
                pass
            if lvl >= 50:
                anws = (f'{anws}\n:puzzle_piece:<b>Парагонов</b> {paragon}({for_stat(paragon,record[6],0)}) ≈ :full_moon:{get_paragon(exp)} до <b>{paragon+1}</b> ')

            if aden-record[18] > 0:
                aden_format = '+{0:,}'.format(aden-record[18]).replace(',', ' ')
            else:
                aden_format = '{0:,}'.format(aden-record[18]).replace(',', ' ')
            if cred-record[21] > 0:
                cred_format = '+{0:,}'.format(cred-record[21]).replace(',', ' ')
            else:
                cred_format = '{0:,}'.format(cred-record[21]).replace(',', ' ')
            if diamond-record[19] > 0:
                diamond_format = '+{0:,}'.format(diamond-record[19]).replace(',', ' ')
            else:
                diamond_format = '{0:,}'.format(diamond-record[19]).replace(',', ' ')

            anws = (f'{anws}\n\n:oncoming_fist_light_skin_tone:{pvp}({for_stat(pvp,record[20],0)}) '
                    f':rosette:{aden_format} :money_bag:{cred_format} :gem_stone:{diamond_format}')

            if abu_mess:
                anws = (f'{anws}\n\n<b>:trackball:Поставь АБУ!</b>')

            arg = username,race,guild,nickname,lvl,paragon,hp,atk,defense,dodge,critical,accuracy,exp,exp_bonus, \
                  prem,prem_abu, message.forward_date,aden,diamond,pvp,cred,eter,kopka,pm,id_user,prof_bel,prof_cor,prof_acr

            await pool.fetch('''UPDATE test.public.user SET username=$1,race=$2,guild=$3,nickname=$4,lvl=$5,
                                                 paragon=$6,hp=$7,atk=$8,def=$9,dodge=$10,crit=$11,accuracy=$12,
                                                 exp=$13,exp_bonus=$14,premium=$15,abu=$16,date_update=$17,aden=$18,
                                                 diamond=$19,pvp=$20,credits=$21,exp_earner=$22,exp_digger=$23,
                                                 user_dialog=$24, last_activity=$17,lvl_prof_bel=$26,lvl_prof_cor=$27,
                                                 lvl_prof_acr=$28
                                                 WHERE id=$25''', *arg)


            await message.answer(emojize(anws))
            await message.delete()
    else:
        await message.reply(f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>\n'
                            f'Сообщение слишком старое! Давай посвежее')
        await message.delete()