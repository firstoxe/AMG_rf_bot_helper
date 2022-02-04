from aiogram import types
from loader import dp
from filters.recipe_update import RecipeUpdate, RecipeUpdateOtherBot
from aiogram.utils.emoji import demojize,emojize
from utils.misc import rate_limit
from asyncpg import Connection, Record
from loader import db
from datetime import datetime
from filters.work_with_user import helper_user
from data.config import admins


@rate_limit(0, 'recipe_update')
@dp.message_handler(RecipeUpdate())
async def recipte_take_foward(message: types.Message):
    if (datetime.now() - message.forward_date).total_seconds() < 3600:
        msg = demojize(message.text).splitlines()
        name_rec = msg[0].split('Рецепт ')[1].lower()
        if name_rec[-1:] == '.':
            name_rec = name_rec[:-1]
        hp = None
        defens = None
        dodge = None
        crit = None
        exp = None
        atk = None
        acc = None
        lvl = None
        kraft_shance = None
        for item in msg:
            if item.find(':red_heart:') != -1:
                hp = int(item.split(' +')[1])
            if item.find(':shield:') != -1:
                defens = int(item.split(' +')[1])
            if item.find(':dashing_away:') != -1:
                dodge = float(item.split(' +')[1][:-1])
            if item.find(':bullseye:') != -1:
                crit = float(item.split(' +')[1][:-1])
            if item.find(':crystal_ball:') != -1:
                exp = float(item.split(' +')[1][:-1])
            if item.find(':crossed_swords:') != -1:
                atk = int(item.split(' +')[1])
            if item.find(':hourglass_not_done:') != -1:
                acc = float(item.split(' +')[1][:-1])
            if item.find('Уровень: ') != -1:
                lvl = int(item.split('Уровень: ')[1])
            if item.find('Шанс крафта: ') != -1:
                kraft_shance = float(item.split('Шанс крафта: ')[1][:-1])
        pool: Connection = db
        recept: Record = await pool.fetchrow('SELECT * FROM test.public.recipes '
                                             'where name=$1 or name_a = $1 or name_b = $1', name_rec,)
        if not recept:
            arg = name_rec, hp, atk, defens, dodge, crit, exp, acc, lvl
            await pool.fetchrow("""INSERT INTO recipes VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)""", *arg)
            await message.answer(f"""{await helper_user(message.from_user.id)}
В базу был добавлен новый рецепт:
<b>{name_rec}</b>""")
        else:
            res = []
            res.append(f'{await helper_user(message.from_user.id)} держи:')
            res.append('')
            res.append(f':scroll:Рецепт <b>{name_rec}</b> :sports_medal:{lvl} ({kraft_shance}%)')
            res.append('')
            new_hp = None
            new_defens = None
            new_dodge = None
            new_crit = None
            new_exp = None
            new_atk = None
            new_acc = None
            new_lvl = None
            if hp:
                if hp > recept["hp"]:
                    new_hp = hp
                    res.append(f':red_heart:{new_hp}({recept["hp"]}): <b>+{new_hp-recept["hp"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET hp=$1 where name=$2""", new_hp, name_rec,)
                if hp == recept["hp"]:
                    res.append(f':red_heart:{hp}({recept["hp"]}): <b>{hp-recept["hp"]}</b>🔝')
                if hp < recept["hp"]:
                    res.append(f':red_heart:{hp}({recept["hp"]}): <b>{hp-recept["hp"]}</b>')
            if atk:
                if atk > recept["atk"]:
                    new_atk = atk
                    res.append(f':crossed_swords:{new_atk}({recept["atk"]}): <b>+{new_atk-recept["atk"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET atk=$1 where name=$2""", new_atk, name_rec,)
                if atk == recept["atk"]:
                    res.append(f':crossed_swords:{atk}({recept["atk"]}): <b>{atk-recept["atk"]}</b>🔝')
                if atk < recept["atk"]:
                    res.append(f':crossed_swords:{atk}({recept["atk"]}): <b>{atk-recept["atk"]}</b>')
            if defens:
                if defens > recept["def"]:
                    new_defens = defens
                    res.append(f':shield:{new_defens}({recept["def"]}): <b>+{new_defens-recept["def"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET def=$1 where name=$2""", new_defens, name_rec,)
                if defens == recept["def"]:
                    res.append(f':shield:{defens}({recept["def"]}): <b>{defens-recept["def"]}</b>🔝')
                if defens < recept["def"]:
                    res.append(f':shield:{defens}({recept["def"]}): <b>{defens-recept["def"]}</b>')
            if dodge:
                if dodge > recept["dodge"]:
                    new_dodge = dodge
                    res.append(f':dashing_away:{new_dodge}({recept["dodge"]}): <b>+{(new_dodge-recept["dodge"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET dodge=$1 where name=$2""", new_dodge, name_rec,)
                if dodge == recept["dodge"]:
                    res.append(f':dashing_away:{dodge}({recept["dodge"]}): <b>{dodge-recept["dodge"]}</b>🔝')
                if dodge < recept["dodge"]:
                    res.append(f':dashing_away:{dodge}({recept["dodge"]}): <b>{(dodge-recept["dodge"]):.{2}f}</b>')
            if acc:
                if acc > recept["acc"]:
                    new_acc = acc
                    res.append(f':hourglass_not_done:{new_acc}({recept["acc"]}): <b>+{(new_acc-recept["acc"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET acc=$1 where name=$2""", new_acc, name_rec,)
                if acc == recept["acc"]:
                    res.append(f':hourglass_not_done:{acc}({recept["acc"]}): <b>{acc-recept["acc"]}</b>🔝')
                if acc < recept["acc"]:
                    res.append(f':hourglass_not_done:{acc}({recept["acc"]}): <b>{(acc-recept["acc"]):.{2}f}</b>')
            if crit:
                if crit > recept["crit"]:
                    new_crit = crit
                    res.append(f':bullseye:{new_crit}({recept["crit"]}): <b>+{(new_crit-recept["crit"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET crit=$1 where name=$2""", new_crit, name_rec,)
                if crit == recept["crit"]:
                    res.append(f':bullseye:{crit}({recept["crit"]}): <b>{crit-recept["crit"]}</b>🔝')
                if crit < recept["crit"]:
                    res.append(f':bullseye:{crit}({recept["crit"]}): <b>{(crit-recept["crit"]):.{2}f}</b>')
            if exp:
                if exp > recept["exp"]:
                    new_exp = exp
                    res.append(f':crystal_ball:{new_exp}({recept["exp"]}): <b>+{(new_exp-recept["exp"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET exp=$1 where name=$2""", new_exp, name_rec,)
                if exp == recept["exp"]:
                    res.append(f':crystal_ball:{exp}({recept["exp"]}): <b>{exp-recept["exp"]}</b>🔝')
                if exp < recept["exp"]:
                    res.append(f':crystal_ball:{exp}({recept["exp"]}): <b>{(exp-recept["exp"]):.{2}f}</b>')
            await message.answer(emojize('\n'.join(res)))
            if message.from_user.id == message.chat.id:
                await message.delete()
            else:
                try:
                    await message.delete()
                except:
                    await message.answer('Не достаточно прав для удаления сообщения!')
    else:
        await message.reply('Сообщение слишком старое!')


@rate_limit(0, 'recipe_update_other')
@dp.message_handler(RecipeUpdateOtherBot(), user_id=admins)
async def recipte_take_foward_other_bot(message: types.Message):
    if message.text.find('Максимальные статы для ') == -1:
        msg = demojize(message.text).lower().splitlines()
        msg.remove(msg[0])
        if message.forward_from.id == 980441353:
            msg.remove(msg[0])
        name_rec = msg[0].split('рецепт ')[1]
        if name_rec[-1:] == '.':
            name_rec = name_rec[:-1]
        hp = None
        defens = None
        dodge = None
        crit = None
        exp = None
        atk = None
        acc = None
        lvl = None
        kraft_shance = None
        for item in msg:
            if item.find(':red_heart:') != -1:
                hp = int(item.split(' (')[1].split(')')[0])
            if item.find(':shield:') != -1:
                defens = int(item.split(' (')[1].split(')')[0])
            if item.find(':dashing_away:') != -1:
                dodge = float(item.split(' (')[1].split(')')[0])
            if item.find(':bullseye:') != -1:
                crit = float(item.split(' (')[1].split(')')[0])
            if item.find(':crystal_ball:') != -1:
                exp = float(item.split(' (')[1].split(')')[0])
            if item.find(':crossed_swords:') != -1:
                atk = int(item.split(' (')[1].split(')')[0])
            if item.find(':hourglass_not_done:') != -1:
                acc = float(item.split(' (')[1].split(')')[0])
            if item.find('уровень: ') != -1:
                lvl = int(item.split('уровень: ')[1])
            if item.find('шанс крафта: ') != -1:
                kraft_shance = float(item.split('шанс крафта: ')[1][:-1])
        pool: Connection = db
        recept: Record = await pool.fetchrow('SELECT * FROM test.public.recipes '
                                             'where name=$1 or name_a = $1 or name_b = $1', name_rec,)
        if not recept:
            arg = name_rec, hp, atk, defens, dodge, crit, exp, acc, lvl
            await pool.fetchrow("""INSERT INTO recipes VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)""", *arg)
            await message.answer(f"""{await helper_user(message.from_user.id)}
В базу был добавлен новый рецепт:
<b>{name_rec}</b>""")
        else:
            res = []
            res.append(f'{await helper_user(message.from_user.id)} держи:')
            res.append('')
            res.append(f':scroll:Рецепт <b>{name_rec}</b> :sports_medal:{lvl} ({kraft_shance}%)')
            res.append('')
            new_hp = None
            new_defens = None
            new_dodge = None
            new_crit = None
            new_exp = None
            new_atk = None
            new_acc = None
            if hp:
                if hp > recept["hp"]:
                    new_hp = hp
                    res.append(f':red_heart:{new_hp}({recept["hp"]}): <b>+{new_hp-recept["hp"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET hp=$1 where name=$2""", new_hp, name_rec,)
                if hp == recept["hp"]:
                    res.append(f':red_heart:{hp}({recept["hp"]}): <b>{hp-recept["hp"]}</b>🔝')
                if hp < recept["hp"]:
                    res.append(f':red_heart:{hp}({recept["hp"]}): <b>{hp-recept["hp"]}</b>')
            if atk:
                if atk > recept["atk"]:
                    new_atk = atk
                    res.append(f':crossed_swords:{new_atk}({recept["atk"]}): <b>+{new_atk-recept["atk"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET atk=$1 where name=$2""", new_atk, name_rec,)
                if atk == recept["atk"]:
                    res.append(f':crossed_swords:{atk}({recept["atk"]}): <b>{atk-recept["atk"]}</b>🔝')
                if atk < recept["atk"]:
                    res.append(f':crossed_swords:{atk}({recept["atk"]}): <b>{atk-recept["atk"]}</b>')
            if defens:
                if defens > recept["def"]:
                    new_defens = defens
                    res.append(f':shield:{new_defens}({recept["def"]}): <b>+{new_defens-recept["def"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET def=$1 where name=$2""", new_defens, name_rec,)
                if defens == recept["def"]:
                    res.append(f':shield:{defens}({recept["def"]}): <b>{defens-recept["def"]}</b>🔝')
                if defens < recept["def"]:
                    res.append(f':shield:{defens}({recept["def"]}): <b>{defens-recept["def"]}</b>')
            if dodge:
                if dodge > recept["dodge"]:
                    new_dodge = dodge
                    res.append(f':dashing_away:{new_dodge}({recept["dodge"]}): <b>+{(new_dodge-recept["dodge"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET dodge=$1 where name=$2""", new_dodge, name_rec,)
                if dodge == recept["dodge"]:
                    res.append(f':dashing_away:{dodge}({recept["dodge"]}): <b>{dodge-recept["dodge"]}</b>🔝')
                if dodge < recept["dodge"]:
                    res.append(f':dashing_away:{dodge}({recept["dodge"]}): <b>{(dodge-recept["dodge"]):.{2}f}</b>')
            if acc:
                if acc > recept["acc"]:
                    new_acc = acc
                    res.append(f':hourglass_not_done:{new_acc}({recept["acc"]}): <b>+{(new_acc-recept["acc"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET acc=$1 where name=$2""", new_acc, name_rec,)
                if acc == recept["acc"]:
                    res.append(f':hourglass_not_done:{acc}({recept["acc"]}): <b>{acc-recept["acc"]}</b>🔝')
                if acc < recept["acc"]:
                    res.append(f':hourglass_not_done:{acc}({recept["acc"]}): <b>{(acc-recept["acc"]):.{2}f}</b>')
            if crit:
                if crit > recept["crit"]:
                    new_crit = crit
                    res.append(f':bullseye:{new_crit}({recept["crit"]}): <b>+{(new_crit-recept["crit"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET crit=$1 where name=$2""", new_crit, name_rec,)
                if crit == recept["crit"]:
                    res.append(f':bullseye:{crit}({recept["crit"]}): <b>{crit-recept["crit"]}</b>🔝')
                if crit < recept["crit"]:
                    res.append(f':bullseye:{crit}({recept["crit"]}): <b>{(crit-recept["crit"]):.{2}f}</b>')
            if exp:
                if exp > recept["exp"]:
                    new_exp = exp
                    res.append(f':crystal_ball:{new_exp}({recept["exp"]}): <b>+{(new_exp-recept["exp"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET exp=$1 where name=$2""", new_exp, name_rec,)
                if exp == recept["exp"]:
                    res.append(f':crystal_ball:{exp}({recept["exp"]}): <b>{exp-recept["exp"]}</b>🔝')
                if exp < recept["exp"]:
                    res.append(f':crystal_ball:{exp}({recept["exp"]}): <b>{(exp-recept["exp"]):.{2}f}</b>')
            if lvl:
                await pool.fetchrow("""UPDATE recipes SET lvl=$1 where name=$2""", lvl, name_rec,)
            await message.answer(emojize('\n'.join(res)))
        if message.from_user.id == message.chat.id:
            await message.delete()
    elif message.text.find('Максимальные статы для ') != -1:
        msg = demojize(message.text).splitlines()
        if message.forward_from.id == 1058325728:
            msg.remove(msg[0])
        name_rec = msg[0].split('Максимальные статы для ')[1]
        if name_rec[-1:] == ':':
            name_rec = name_rec[:-1]
        hp = None
        defens = None
        dodge = None
        crit = None
        exp = None
        atk = None
        acc = None
        lvl = None
        for item in msg:
            if item.find(':red_heart:') != -1:
                hp = int(item.split(':red_heart:')[1])
            if item.find(':shield:') != -1:
                defens = int(item.split(':shield:')[1])
            if item.find(':dashing_away:') != -1:
                dodge = float(item.split(':dashing_away:')[1])
            if item.find(':bullseye:') != -1:
                crit = float(item.split(':bullseye:')[1])
            if item.find(':crystal_ball:') != -1:
                exp = float(item.split(':crystal_ball:')[1])
            if item.find(':crossed_swords:') != -1:
                atk = int(item.split(':crossed_swords:')[1])
            if item.find(':hourglass_not_done:') != -1:
                acc = float(item.split(':hourglass_not_done:')[1])
        pool: Connection = db
        recept: Record = await pool.fetchrow('SELECT * FROM test.public.recipes '
                                             'where name=$1 or name_a = $1 or name_b = $1', name_rec,)
        if not recept:
            arg = name_rec, hp, atk, defens, dodge, crit, exp, acc
            await pool.fetchrow("""INSERT INTO recipes VALUES ($1,$2,$3,$4,$5,$6,$7,$8)""", *arg)
            await message.answer(f"""{await helper_user(message.from_user.id)}
В базу был добавлен новый рецепт:
<b>{name_rec}</b>""")
        else:
            res = []
            res.append(f'{await helper_user(message.from_user.id)}</a> макс статы обновлены:')
            res.append('')
            new_hp = None
            new_defens = None
            new_dodge = None
            new_crit = None
            new_exp = None
            new_atk = None
            new_acc = None
            new_lvl = None
            if hp:
                if hp > recept["hp"]:
                    new_hp = hp
                    res.append(f':red_heart:{new_hp}({recept["hp"]}): <b>+{new_hp-recept["hp"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET hp=$1 where name=$2""", new_hp, name_rec,)
                if hp == recept["hp"]:
                    res.append(f':red_heart:{hp}({recept["hp"]}): <b>{hp-recept["hp"]}</b>🔝')
                if hp < recept["hp"]:
                    res.append(f':red_heart:{hp}({recept["hp"]}): <b>{hp-recept["hp"]}</b>')
            if atk:
                if atk > recept["atk"]:
                    new_atk = atk
                    res.append(f':crossed_swords:{new_atk}({recept["atk"]}): <b>+{new_atk-recept["atk"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET atk=$1 where name=$2""", new_atk, name_rec,)
                if atk == recept["atk"]:
                    res.append(f':crossed_swords:{atk}({recept["atk"]}): <b>{atk-recept["atk"]}</b>🔝')
                if atk < recept["atk"]:
                    res.append(f':crossed_swords:{atk}({recept["atk"]}): <b>{atk-recept["atk"]}</b>')
            if defens:
                if defens > recept["def"]:
                    new_defens = defens
                    res.append(f':shield:{new_defens}({recept["def"]}): <b>+{new_defens-recept["def"]}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET def=$1 where name=$2""", new_defens, name_rec,)
                if defens == recept["def"]:
                    res.append(f':shield:{defens}({recept["def"]}): <b>{defens-recept["def"]}</b>🔝')
                if defens < recept["def"]:
                    res.append(f':shield:{defens}({recept["def"]}): <b>{defens-recept["def"]}</b>')
            if dodge:
                if dodge > recept["dodge"]:
                    new_dodge = dodge
                    res.append(f':dashing_away:{new_dodge}({recept["dodge"]}): <b>+{(new_dodge-recept["dodge"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET dodge=$1 where name=$2""", new_dodge, name_rec,)
                if dodge == recept["dodge"]:
                    res.append(f':dashing_away:{dodge}({recept["dodge"]}): <b>{dodge-recept["dodge"]}</b>🔝')
                if dodge < recept["dodge"]:
                    res.append(f':dashing_away:{dodge}({recept["dodge"]}): <b>{(dodge-recept["dodge"]):.{2}f}</b>')
            if acc:
                if acc > recept["acc"]:
                    new_acc = acc
                    res.append(f':hourglass_not_done:{new_acc}({recept["acc"]}): <b>+{(new_acc-recept["acc"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET acc=$1 where name=$2""", new_acc, name_rec,)
                if acc == recept["acc"]:
                    res.append(f':hourglass_not_done:{acc}({recept["acc"]}): <b>{acc-recept["acc"]}</b>🔝')
                if acc < recept["acc"]:
                    res.append(f':hourglass_not_done:{acc}({recept["acc"]}): <b>{(acc-recept["acc"]):.{2}f}</b>')
            if crit:
                if crit > recept["crit"]:
                    new_crit = crit
                    res.append(f':bullseye:{new_crit}({recept["crit"]}): <b>+{(new_crit-recept["crit"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET crit=$1 where name=$2""", new_crit, name_rec,)
                if crit == recept["crit"]:
                    res.append(f':bullseye:{crit}({recept["crit"]}): <b>{crit-recept["crit"]}</b>🔝')
                if crit < recept["crit"]:
                    res.append(f':bullseye:{crit}({recept["crit"]}): <b>{(crit-recept["crit"]):.{2}f}</b>')
            if exp:
                if exp > recept["exp"]:
                    new_exp = exp
                    res.append(f':crystal_ball:{new_exp}({recept["exp"]}): <b>+{(new_exp-recept["exp"]):.{2}f}</b>✨')
                    await pool.fetchrow("""UPDATE recipes SET exp=$1 where name=$2""", new_exp, name_rec,)
                if exp == recept["exp"]:
                    res.append(f':crystal_ball:{exp}({recept["exp"]}): <b>{exp-recept["exp"]}</b>🔝')
                if exp < recept["exp"]:
                    res.append(f':crystal_ball:{exp}({recept["exp"]}): <b>{(exp-recept["exp"]):.{2}f}</b>')
            await message.answer(emojize('\n'.join(res)))
        if message.from_user.id == message.chat.id:
            await message.delete()
