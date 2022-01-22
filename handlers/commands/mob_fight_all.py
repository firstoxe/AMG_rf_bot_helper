from aiogram import types
from loader import dp, db
from aiogram.types.chat import ChatType
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import demojize,emojize
from data.config import admins
from utils.misc import rate_limit
import random
from filters.guild_check import check_g

mob_loc = [['Флем', 2, 31, 36, 4, 4, 15, 15],
           ['Вертобот', 3, 55, 40, 4, 4, 20, 25],
           ['Клаан', 4, 77, 42, 7, 4, 20, 35],
           ['Навозник', 5, 110, 45, 6, 4, 15, 45],
           ['Стригой', 6, 149, 49, 8, 4, 15, 55],
           ['Саблезуб', 7, 182, 52, 10, 4, 20, 60],
           ['Старший Стригой', 8, 2555, 68, 11, 4, 15, 65],
           ['Ратозверь', 9, 280, 74, 14, 4, 20, 75],
           ['Молотоглав', 10, 350, 95, 18, 4, 20, 85],
           ['Мехозавр', 11, 370, 100, 17, 4, 15, 95],
           ['Змееголов', 12, 400, 107, 18, 4, 15, 100],
           ['Призрак', 13, 420, 115, 20, 4, 15, 115],
           ['Скарабей', 14, 440, 123, 25, 4, 15, 130],
           ['Культист', 15, 460, 135, 27, 4, 15, 145],
           ['Богомол', 16, 500, 150, 28, 4, 15, 160],
           ['Ящер', 17, 520, 155, 28, 4, 15, 170],
           ['Культист воин', 18, 550, 168, 28, 4, 15, 200],
           ['Высший Скарабей', 19, 650, 195, 30, 4, 15, 210],
           ['Песчаный червь', 20, 680, 220, 31, 4, 15, 220],
           ['Скарабей секач', 21, 700, 250, 34, 4, 11, 260],
           ['Трицератопс', 22, 710, 255, 35, 4, 11, 300],
           ['Трицератопс каннибал', 23, 720, 260, 36, 4, 11, 330],
           ['Наяда', 24, 780, 265, 37, 4, 11, 360],
           ['Слизень', 25, 800, 270, 38, 4, 11, 370],
           ['Наяда принцесса', 26, 820, 280, 39, 4, 11, 385],
           ['Калина', 27, 860, 290, 40, 4, 11, 395],
           ['Доспех-призрак', 28, 890, 315, 45, 4, 11, 400],
           ['Королевская креветка', 29, 920, 380, 46, 4, 11, 410],
           ['Бельфегор', 30, 990, 400, 55, 4, 11, 440],
           ['Гиперморф', 31, 1100, 450, 55, 4, 15, 480],
           ['Красный Скорпион', 32, 1250, 460, 60, 4, 15, 515],
           ['Ундина', 33, 1300, 470, 63, 4, 15, 530],
           ['Черный Песчаный Червь', 34, 1400, 480, 70, 4, 15, 560],
           ['Шутти', 35, 1430, 490, 75, 4, 15, 590],
           ['Калиана Убийца', 36, 1470, 500, 78, 4, 15, 610],
           ['Альфа', 37, 1550, 510, 78, 4, 15, 630],
           ['Вулканический Скарабей', 38, 1570, 570, 80, 4, 15, 650],
           ['Магмоид', 39, 1600, 600, 80, 4, 15, 670],
           ['Злой Септим', 40, 1650, 620, 85, 4, 15, 700],
           ['Бета', 41, 1750, 650, 87, 4, 15, 710],
           ['Сверкающий Мотылек', 42, 1850, 700, 90, 4, 15, 730],
           ['Птенец Псевдодракона', 43, 1900, 720, 93, 4, 15, 750],
           ['Предводитель гоблинов', 44, 1950, 830, 97, 4, 15, 760],
           ['Псевдодракон', 45, 1970, 890, 102, 4, 15, 770],
           ['Орк предводитель', 46, 2000, 960, 105, 4, 15, 780],
           ['Саблезуб Матриарх', 47, 2050, 1100, 110, 4, 15, 800],
           ['Ренегат Медиум', 48, 2100, 1250, 113, 4, 15, 810],
           ['Ренегат Каратель', 49, 2150, 1400, 117, 4, 15, 850],
           ['Ренегат Берсерк', 50, 2200, 1500, 125, 4, 15, 900],
           ['Гладиатор', 51, 2350, 1700, 150, 20, 20, 1050,15],
           ['Кровавый Раптор', 52, 2500, 1800, 150, 20, 20, 1250,15],
           ['Элефант', 53, 3125, 1900, 170, 20, 20, 1500, 20],
           ['Разрушитель Рии', 54, 3250, 1985, 170, 20, 20, 1750, 20],
           ['Тераон', 55, 3800, 2050, 200, 20, 20, 2100, 30],
           ['Лазурный клаан', 56, 4300, 2200, 260, 20, 20, 2350, 30],
           ['Тор наемник', 57, 4400, 2283, 275, 20, 20, 2600, 30],
           ['Каменный воин', 58, 4950, 2412, 335, 20, 20, 2850, 30],
           ['Спектр', 59, 5200, 2500, 370, 20, 20, 3100, 30],
           ['Нарум', 60, 5800, 2735, 420, 25, 20, 3450, 30]]

mob_eter = [['Бронзовый Голем', 9, 350, 100, 15, 4, 15, 0, 0],
            ['Серебряный Голем', 19, 650, 195, 30, 4, 15, 0, 0],
            ['Золотой Голем', 29, 950, 500, 45, 4, 15, 0, 0],
            ['Платиновый Голем', 39, 1970, 830, 102, 4, 15, 0, 0],
            ['Кристальный Голем', 49, 2000, 1500, 135, 4, 15, 0, 0],
            ['Изумрудный Голем', 53, 3250, 1930, 175, 20, 20, 0, 30],
            ['Сапфировый Голем', 58, 4950, 2412, 335, 20, 20, 0, 30]]


async def mob_figth(mob,id,loc):
    pool: Connection = db
    user: Record = await pool.fetchrow('''SELECT id,guild,nickname,atk,def,hp,dodge,crit,accuracy,exp_bonus,lvl,premium from test.public."user" where id=$1''', id,)
    hp_user = user["hp"]
    if loc == 'eter':
        for item in mob_eter:
            if item[1] == int(mob):
                stat_mob = item
    elif loc == 'loc':
        for item in mob_loc:
            if item[1] == int(mob):
                stat_mob = item
    hp_mob = stat_mob[2]
    result = []

    result.append(emojize(f'<b>[{user["lvl"]}]</b>{check_g(user["guild"])}<a href="tg://user?id={user["id"]}">'
                                  f'{emojize(user["nickname"])}</a>❤{hp_user:.{0}f} 🆚 '
                                  f'[{stat_mob[1]}]{stat_mob[0]}❤{hp_mob:.{0}f}\n'))
    pobed = 0
    poraj = 0
    if user["atk"] <= stat_mob[4]:
        atk = stat_mob[4]
    else:
        atk = user["atk"] - stat_mob[4]
    cc = 0

    if stat_mob[3] <= user["def"]:
        atk_mob = 0
    else:
        atk_mob = stat_mob[3] - user["def"]
    crit_usr = atk + int(f"{(atk / 100 * 40):.{0}f}")
    crit_usr_sh = user['crit']
    crit_mob = atk_mob + int(f"{atk_mob / 100 * 40:.{0}f}")
    crit_mob_sh = stat_mob[6]
    if stat_mob[1] <51:
        dodge_usr = 100 * int(f"{user['dodge']:.{0}f}")
    else:
        dodge_usr = int(f"{(100 * user['dodge'])-stat_mob[8]*100:.{0}f}")
    dodge_usr_sh = dodge_usr / 100
    dodge_mob = int(f"{100 * stat_mob[5] - user['accuracy'] * 100:.{0}f}")
    if dodge_mob <= user['accuracy'] * 100:
        dodge_mob = 0

    dodge2_mob_sh = dodge_mob / 100
    first_batle = False

    stats_user_dodge = 0
    stats_user_crit = 0
    stats_user_hp = 0
    stats_user_send_damage = 0
    stats_mob_dodge = 0
    stats_mob_send_damage = 0
    while True:
        if cc == 10000:
            break
        else:
            cc += 1
        dead = False
        hp_mob_fight = hp_mob
        usr_mob_fight = hp_user
        if random.randrange(start=1, stop=10000, step=1) < 300:
            while hp_mob_fight > 0 and usr_mob_fight > 0:
                ra = random.randrange(1, 10000, 1) / 100
                if ra > dodge2_mob_sh:
                    ra = random.randrange(1, 10000, 1) / 100
                    if ra <= crit_usr_sh:
                        hp_mob_fight -= crit_usr
                        stats_user_crit += 1
                        if not first_batle:
                            result.append(f"Ты нанёс удар 💫{crit_usr:.{0}f}")
                    else:
                        hp_mob_fight -= atk
                        stats_user_send_damage += 1
                        if not first_batle:
                            result.append(f"Ты нанёс удар 💥{atk:.{0}f}")
                else:
                    hp_mob_fight -= 0
                    stats_mob_dodge += 1
                    if not first_batle:
                        result.append(f"<b>{stat_mob[0]}</b> увернулся от атаки 💨")
                if hp_mob_fight <= 0:
                    pobed += 1
                    break

                ra = random.randrange(1, 10000, 1) / 100
                if ra > dodge_usr_sh:
                    ra = random.randrange(1, 10000, 1) / 100
                    if ra <= crit_mob_sh:
                        usr_mob_fight -= crit_mob
                        stats_mob_send_damage += 1
                        if not first_batle:
                            result.append(f"<b>{stat_mob[0]}</b> нанёс удар 💔💫{crit_mob:.{0}f}")
                    else:
                        usr_mob_fight -= atk_mob
                        stats_mob_send_damage += 1
                        if not first_batle:
                            result.append(f"<b>{stat_mob[0]}</b> нанёс удар 💔{atk_mob:.{0}f}")
                else:
                    usr_mob_fight -= 0
                    stats_user_dodge += 1
                    if not first_batle:
                        result.append(f"Ты увернулся от атаки 💨")
                if usr_mob_fight <= 0:
                    poraj += 1
                    dead = True
                    break
        else:
            while hp_mob_fight > 0 and usr_mob_fight > 0:
                ra = random.randrange(1, 10000, 1) / 100
                if ra > dodge_usr_sh:
                    ra = random.randrange(1, 10000, 1) / 100
                    if ra <= crit_mob_sh:
                        usr_mob_fight -= crit_mob
                        stats_mob_send_damage += 1
                        if not first_batle:
                            result.append(f"<b>{stat_mob[0]}</b> нанёс удар 💔💫{crit_mob:.{0}f}")
                    else:
                        usr_mob_fight -= atk_mob
                        stats_mob_send_damage += 1
                        if not first_batle:
                            result.append(f"<b>{stat_mob[0]}</b> нанёс удар 💔{atk_mob:.{0}f}")
                else:
                    usr_mob_fight -= 0
                    stats_user_dodge += 1
                    if not first_batle:
                        result.append(f"Ты увернулся от атаки 💨")
                if usr_mob_fight <= 0:
                    poraj += 1
                    dead = True
                    break
                ra = random.randrange(1, 10000, 1) / 100
                if ra > dodge2_mob_sh:
                    ra = random.randrange(1, 10000, 1) / 100
                    if ra <= crit_usr_sh:
                        if usr_mob_fight > 0:
                            hp_mob_fight -= crit_usr
                            stats_user_crit += 1
                            if not first_batle:
                                result.append(f"Ты нанёс удар 💫{crit_usr:.{0}f}")
                    else:
                        if usr_mob_fight > 0:
                            hp_mob_fight -= atk
                            stats_user_send_damage += 1
                            if not first_batle:
                                result.append(f"Ты нанёс удар 💥{atk:.{0}f}")
                else:
                    if usr_mob_fight >0:
                        hp_mob_fight -= 0
                        stats_mob_dodge += 1
                        if not first_batle:
                            result.append(f"<b>{stat_mob[0]}</b> увернулся от атаки 💨")
                if hp_mob_fight <= 0:
                    pobed += 1
                    break
        if not first_batle:
            result.append(f'\nОсталось 💖хп - {usr_mob_fight:.{0}f}')
        first_batle = True
        if not dead:
            stats_user_hp += usr_mob_fight

    result.append(f'\n🏆Шанс победы - {pobed / 10000 * 100:.{2}f}%')
    result.append(f'💫Шанс крита - {stats_user_crit / (stats_user_crit+stats_user_send_damage) * 100:.{2}f}%')
    result.append(f'💨Шанс уворота - {stats_user_dodge / (stats_mob_send_damage+stats_user_dodge) * 100:.{2}f}%')
    result.append(f'⏳Шанс промаха - {stats_mob_dodge  / (stats_user_send_damage+stats_user_crit+stats_mob_dodge) * 100:.{2}f}%')
    try:
        result.append(f'💖Среднее остаточное хп - {stats_user_hp  / (pobed*hp_user) * 100:.{2}f}% ({hp_user*(stats_user_hp  / (pobed*hp_user) * 100)/100:.{0}f})')
    except:
        pass
    if loc == 'loc':
        if user["premium"] != None and datetime.now().date() <= user["premium"]:
            result.append(f'🔮 Опыт - {(stat_mob[7] + (stat_mob[7]/100*user["exp_bonus"])*pobed/10000):.{0}f}/{(stat_mob[7]+(stat_mob[7]/100*user["exp_bonus"])):.{0}f} '
                          f'| в час {(stat_mob[7] + (stat_mob[7]/100*user["exp_bonus"])*pobed/10000)*3:,.{0}f}'.replace(',',' '))
        else:
            result.append(f'🔮 Опыт - {((stat_mob[7] + (stat_mob[7]/100*user["exp_bonus"]))*pobed/3000):,.{0}f}/{(stat_mob[7]+(stat_mob[7]/100*user["exp_bonus"])):.{0}f} '
                          f'| в час {(stat_mob[7] + (stat_mob[7]/100*user["exp_bonus"])*pobed/10000)*2:,.{0}f}'.replace(',',' '))
    result.append(f'\nДанные результаты расчитываются из 10 000 симуляций')
    result.append(f'\nПовторить симуляцию через кнопку обновить можно с интеравлом в 3 секунды')
    result = '\n'.join(result)
    return result


async def mob_exp_top(id):
    pool: Connection = db
    user: Record = await pool.fetchrow('''SELECT id,guild,nickname,atk,def,hp,dodge,crit,accuracy,exp_bonus,lvl,premium from test.public."user" where id=$1''', int(id),)


    stat_mob = mob_loc[user['lvl'] - 2]
    stat_list_mob = []
    list_comp_battle = []
    if stat_mob[1] > 6 and stat_mob[1] < 56:
        for item in mob_loc:
            if item[1] >= user['lvl']-4 and item[1] <= user['lvl'] + 5:
                stat_list_mob.append(item)
    elif stat_mob[1] < 6 or stat_mob[1] == 3:
        for item in mob_loc:
            if item[1] >= 6 and item[1] <= 11:
                stat_list_mob.append(item)
    elif stat_mob[1] > 55 or stat_mob[1] == 60:
        for item in mob_loc:
            if item[1] >= 51 and item[1] <= 60:
                stat_list_mob.append(item)

    result = []
    result.append(emojize(f'<b>[{user["lvl"]}]</b>{check_g(user["guild"])}<a href="tg://user?id={user["id"]}">'
                          f'{emojize(user["nickname"])}</a> топ мобов по опыту для твоего уровня:\n\n'))

    for item in stat_list_mob:
        hp_user = user["hp"]
        stat_mob = item
        hp_mob = stat_mob[2]
        pobed = 0
        poraj = 0
        if user["atk"] <= stat_mob[4]:
            atk = stat_mob[4]
        else:
            atk = user["atk"] - stat_mob[4]
        cc = 0

        if stat_mob[3] <= user["def"]:
            atk_mob = 0
        else:
            atk_mob = stat_mob[3] - user["def"]
        crit_usr = atk + int(f"{(atk / 100 * 40):.{0}f}")
        crit_usr_sh = user['crit']
        crit_mob = atk_mob + int(f"{atk_mob / 100 * 40:.{0}f}")
        crit_mob_sh = stat_mob[6]
        if stat_mob[1] <51:
            dodge_usr = 100 * int(f"{user['dodge']:.{0}f}")
        else:
            dodge_usr = int(f"{(100 * user['dodge'])-stat_mob[8]*100:.{0}f}")
        dodge_usr_sh = dodge_usr / 100
        dodge_mob = int(f"{100 * stat_mob[5] - user['accuracy'] * 100:.{0}f}")
        if dodge_mob <= user['accuracy'] * 100:
            dodge_mob = 0

        dodge2_mob_sh = dodge_mob / 100

        while True:
            if cc == 3000:

                break
            else:
                cc += 1
            hp_mob_fight = hp_mob
            usr_mob_fight = hp_user
            if random.randrange(start=1, stop=10000, step=1) < 300:
                while hp_mob_fight > 0 and usr_mob_fight > 0:
                    ra = random.randrange(1, 10000, 1) / 100
                    if ra > dodge2_mob_sh:
                        ra = random.randrange(1, 10000, 1) / 100
                        if ra <= crit_usr_sh:
                            hp_mob_fight -= crit_usr
                        else:
                            hp_mob_fight -= atk
                    else:
                        hp_mob_fight -= 0
                    if hp_mob_fight <= 0:
                        pobed += 1
                        break

                    ra = random.randrange(1, 10000, 1) / 100
                    if ra > dodge_usr_sh:
                        ra = random.randrange(1, 10000, 1) / 100
                        if ra <= crit_mob_sh:
                            usr_mob_fight -= crit_mob
                        else:
                            usr_mob_fight -= atk_mob
                    else:
                        usr_mob_fight -= 0
                    if usr_mob_fight <= 0:
                        poraj += 1
                        break
            else:
                while hp_mob_fight > 0 and usr_mob_fight > 0:
                    ra = random.randrange(1, 10000, 1) / 100
                    if ra > dodge_usr_sh:
                        ra = random.randrange(1, 10000, 1) / 100
                        if ra <= crit_mob_sh:
                            usr_mob_fight -= crit_mob
                        else:
                            usr_mob_fight -= atk_mob
                    else:
                        usr_mob_fight -= 0
                    if usr_mob_fight <= 0:
                        poraj += 1
                        break
                    ra = random.randrange(1, 10000, 1) / 100
                    if ra > dodge2_mob_sh:
                        ra = random.randrange(1, 10000, 1) / 100
                        if ra <= crit_usr_sh:
                            if usr_mob_fight > 0:
                                hp_mob_fight -= crit_usr
                        else:
                            if usr_mob_fight > 0:
                                hp_mob_fight -= atk
                    else:
                        if usr_mob_fight >0:
                            hp_mob_fight -= 0
                    if hp_mob_fight <= 0:
                        pobed += 1
                        break

        list_comp_battle.append(f'[{stat_mob[1]}]<b>{stat_mob[0]}</b> <code>-></code> {pobed / 3000 * 100:.{2}f}% <code>-></code> 🔮'
                                f'{((stat_mob[7] + (stat_mob[7]/100*user["exp_bonus"]))*pobed/3000):,.{0}f}/'
                                f'{(stat_mob[7]+(stat_mob[7]/100*user["exp_bonus"])):,.{0}f}'.replace(',', ' '))
    def keyFunc(item):
        return float((item.split('<code>-></code> 🔮')[1].split('/')[0]).replace(' ', ''))

    list_comp_battle.sort(key=keyFunc, reverse=True)
    return emojize('\n'.join(result) + '\n'.join(list_comp_battle) + '\n\nДанные результаты расчитываются из '
                                                                     '3 000 симуляций для каждого моба\n\nПовторить '
                                                                     'симуляцию можно с интеравлом в 5 секунд нажав на '
                                                                     'кнопку 🔮 Топ мобов по опыту')

