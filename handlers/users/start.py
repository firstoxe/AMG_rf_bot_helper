from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.misc import rate_limit
from loader import dp, db
from datetime import datetime
from asyncpg import Connection, Record
from aiogram.utils.emoji import emojize
from filters.guild_check import check_g

@rate_limit(2, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    arg = message.from_user.id
    pool: Connection = db
    record: Record = await pool.fetchrow('''SELECT id,guild,nickname,user_dialog FROM test.public.user WHERE id = $1''', arg,)

    if not record:
        anws = f'Привет, <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>!'
        arg = message.from_user.id, message.date, message.from_user.username, datetime.now()
        await pool.fetch('''INSERT INTO test.public.user(id, date_update, username, last_activity) values ($1,$2,$3,$4)''', *arg)
        await pool.fetch('''INSERT INTO test.public.notify(id_user) values ($1)''', message.from_user.id,)
        arg_tot = message.from_user.id,0
        await pool.fetch('''INSERT INTO test.public.totems(id_user, atk, atk_a, atk_b, atk_s, atk_g, 
                                                               def, def_a, def_b, def_s, def_g, 
                                                               hp, hp_a, hp_b, hp_s, hp_g, 
                                                               dodge, dodge_a, dodge_b, dodge_s, dodge_g, 
                                                               crit, crit_a, crit_b, crit_s, crit_g, 
                                                               acc, acc_a, acc_b, acc_s, acc_g) 
                                values  ($1,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,$2,
                                        $2,$2,$2,$2,$2,$2,$2,$2,$2,$2)''', *arg_tot)
        await pool.fetch('''INSERT INTO test.public.top_conf(id_user) values ($1)''', message.from_user.id,)
    else:
        if not record[3]:
            arg = True, message.from_user.id
            await pool.fetch('''UPDATE test.public.user SET user_dialog=$1 WHERE id=$2''', *arg)
        arg = message.from_user.username, message.from_user.id, datetime.now()
        await pool.fetch('''UPDATE test.public.user SET username=$1, last_activity=$3 WHERE id=$2''', *arg)
        anws = (f'Привет, <b>{check_g(record[1])}<a href="tg://user?id={record[0]}">{record[2]}</a></b>!')
    anws=(f'{anws}\nДля корректной работы, перешли мне свой <b>профиль из игры</b> @rf_telegram_bot (<a href="http://t.me/share/url?url=/hero">/hero</a>)\n\n'
          f':open_book:Вот список моих возможностей:\n'
          f':sports_medal:Показываю изменения в профиле с последнего обновления(для просмотра своего профиля - /me)\n'
          f':hourglass_not_done:Ежедневные задания и рейтинг (<a href="http://t.me/share/url?url=/daily">/daily</a>)\n'
          f':scroll:Сравнение рецептов и предметов с базой\n'
          f':performing_arts:Настраивать и рассылать приглашения в данжи и пещеры\n'
          f':performing_arts:Помогаю руководить данжами и пещерами\n'
          f':gear:Возможноcть включить и отключить любые уведомления от меня - /config\n'
          f':gear:Ограничения функционала в чате - /config\n'
          f':person_running_light_skin_tone:Пинговать тех, кто находится не в ген. штабе (в чате или ЛС)\n'
          f':church:Пинговать свою гильдию в чате /ping_guild\n'
          f':person_gesturing_NO:Ограничивать общение в чате (только для админов чата) /ro и /unro\n'
          f':speaker_high_volume:Триггеры для чатов (+trigger name / -trigger name / /trigger)\n'
          f':ballot_box_with_ballot:Подсчитывать количество голосов за лидера расы\n'
          f':castle:Помогаю отслеживать битвы за замки и возможость сохранять и просматривать статистику\n'
          f':joystick:Возможность быстрого создания и управление собственным ПУ\n'
          f':alien_monster:Симуляция боя с мобами (/mob) и игроками (/pvp)\n'
          f':moai:Полная сводка по прокачке тотемов /totems\n'
          f':mountain_cableway:Показываю всех, кто находится в пещерах - /cave\n'
          f':mountain_cableway:Отслеживание подъёма и спуска групп в пещерах из твоей лиги\n'
          f':circus_tent:Конвертирую ссылки для аукциона\n'
          f':exclamation_mark:Уведомляю о появление :T-Rex:стража, начале:volcano:войны и :crossed_swords:арены\n'
          f':superhero:‍:male_sign:Просмотр топов по различным категориям и рейтинг гильдий\n'
          f':castle:Просмотр состава гильдии - /list_guild\n'
          f':battery:Расчитываю кап энки\n'
          f':paw_prints:Показываю время прибытия в локацию и время :baby_angel:воскрешения после смерти\n'
          f':clipboard:Просмотр истории смены ника по ид или нику игрока\n'
          f':sunglasses:Получение ссылки на профиль по ид или нику\n'
          f''
          f'<b>Более подробно о всех возможностях, можно почитать в /help</b>\n\n'
          f'')





    await message.answer(emojize(anws))


