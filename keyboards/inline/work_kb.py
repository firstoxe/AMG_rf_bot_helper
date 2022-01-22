from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record
from loader import db, dp
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.callback_data import CallbackData
from datetime import datetime


dat_work_resourse_sel = CallbackData('work_resourse_sel', 'action', 'id', 'date')

async def create_cb_work_resource_sel(id, date):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton('☣️Ядерная энергия', callback_data=dat_work_resourse_sel.new('1', str(id), str(date).replace(':', ';'))),
           InlineKeyboardButton('🏺Потусторонняя энергия', callback_data=dat_work_resourse_sel.new('2', str(id), str(date).replace(':', ';'))),
           InlineKeyboardButton('⚗️Темная материя', callback_data=dat_work_resourse_sel.new('3', str(id), str(date).replace(':', ';'))))
    return kb

dat_work_resourse_page = CallbackData('work_resourse_sel', 'action', 'id', 'date', 'page', 'res')

async def create_cb_work_resource_page(id, date, page, resource):
    pool: Connection = db
    arg = int(page)*5, int(resource)
    all_works: Record = await pool.fetch(f"SELECT * from test.public.contract where race_res=$2 limit 5 offset $1", *arg)
    kb = InlineKeyboardMarkup(row_width=2)
    if all_works:
        if page < 2:
            kb.add(InlineKeyboardButton('➡️', callback_data=dat_work_resourse_page.new('next', str(id), str(date).replace(':', ';'),str(page),str(resource))))
            kb.add(InlineKeyboardButton('🔙', callback_data=dat_work_resourse_page.new('back', str(id), str(date).replace(':', ';'),str(page),str(resource))))
        elif page > 1:
            kb.add(InlineKeyboardButton('⬅️', callback_data=dat_work_resourse_page.new('prev', str(id), str(date).replace(':', ';'),str(int(page)-1),str(resource))),
                   InlineKeyboardButton('➡️', callback_data=dat_work_resourse_page.new('next', str(id), str(date).replace(':', ';'),str(page),str(resource))))
            kb.add(InlineKeyboardButton('🔙', callback_data=dat_work_resourse_page.new('back', str(id), str(date).replace(':', ';'),str(page),str(resource))))
    else:
        if page > 1:
            kb.add(InlineKeyboardButton('⬅️', callback_data=dat_work_resourse_page.new('prev', str(id), str(date).replace(':', ';'),str(int(page)-1),str(resource))))
        kb.add(InlineKeyboardButton('🔙', callback_data=dat_work_resourse_page.new('back', str(id), str(date).replace(':', ';'),str(page),str(resource))))
    return kb


@dp.callback_query_handler(dat_work_resourse_sel.filter(action=['1', '2', '3']))
async def inline_kb_update_works_sel_contract(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            pool: Connection = db
            all_works: Record = await pool.fetch("SELECT * from test.public.contract where race_res=$1 limit 5", int(callback_data["action"]),)
            if all_works:
                anws = f'Доступно контрактов - {await pool.fetchval("SELECT count(id) from test.public.contract where race_res=$1", int(callback_data["action"]),)}\n\n'
                list_works = []
                find_user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', int(callback_data["id"]),)
                for item in all_works:
                    work_time_dict = {1: 15, 2: 9, 3: 4, 4: 2, 5: 1}
                    if int(callback_data["action"]) == 1:
                        work_time = work_time_dict[find_user["lvl_prof_bel"]]*item["amount"]
                    elif int(callback_data["action"]) == 2:
                        work_time = work_time_dict[find_user["lvl_prof_cor"]]*item["amount"]
                    elif int(callback_data["action"]) == 3:
                        work_time = work_time_dict[find_user["lvl_prof_acr"]]*item["amount"]
                    list_works.append(emojize(f'[{item["user_guild"]}]<a href="tg://user?id={item["user_id"]}">{item["user_nickname"]}</a>\n'
                                              f'⛓ Количество: {item["amount"]}ед.\n'
                                              f'🕑 Время работы: {work_time}ч.\n'
                                              f'🏵 Стоимость за 1: {item["price"]:,.{0}f} ({item["price"]*item["amount"]:,.{0}f})\n'
                                              f'✅ Принять контракт - <a href="http://t.me/share/url?url={item["link"]}">{item["link"]}</a>\n'.replace(',', ' ')))

                await query.bot.edit_message_text(text=anws+'\n'.join(list_works),
                                                  chat_id=query.message.chat.id,
                                                  message_id=query.message.message_id,
                                                  reply_markup=await create_cb_work_resource_page(callback_data["id"],callback_data_time,1,int(callback_data["action"])))

            else:
                await query.bot.edit_message_text(text='Извини, но тут нет доступных контрактов на данный момент!',
                                                  chat_id=query.message.chat.id,
                                                  message_id=query.message.message_id,
                                                  reply_markup=await create_cb_work_resource_page(callback_data["id"],callback_data_time,1,int(callback_data["action"])))
            await query.answer(cache_time=2)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=5)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /find_contract для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)


@dp.callback_query_handler(dat_work_resourse_page.filter(action=['back']))
async def inline_kb_update_works_back(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            pool: Connection = db
            find_user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', int(callback_data["id"]),)
            work_time_dict = {1: 15, 2: 9, 3: 4, 4: 2, 5: 1}
            anws = (f'Здесь ты можешь найти заказы на работу\n'
                    f'\n'
                    f'<b>Твоя скорость работы:</b>\n'
                    f'☣️Ядерная энергия - {work_time_dict[find_user["lvl_prof_bel"]]}ч.\n'
                    f'🏺Потусторонняя энергия - {work_time_dict[find_user["lvl_prof_cor"]]}ч.\n'
                    f'⚗️Темная материя - {work_time_dict[find_user["lvl_prof_acr"]]}ч.\n\n'
                    f''
                    f'Количество заказов в базе - {await pool.fetchval("SELECT count(link) from test.public.contract")}\n'
                    f'☣️ - {await pool.fetchval("SELECT count(link) from test.public.contract where race_res=1")}\n'
                    f'🏺 - {await pool.fetchval("SELECT count(link) from test.public.contract where race_res=2")}\n'
                    f'⚗️ - {await pool.fetchval("SELECT count(link) from test.public.contract where race_res=3")}\n\n'
                    f''
                    f'Выбери тип ресурса')
            await query.bot.edit_message_text(text=anws,
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id,
                                              reply_markup=await create_cb_work_resource_sel(callback_data["id"],callback_data_time))
            await query.answer(cache_time=2)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=5)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /find_contract для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)


@dp.callback_query_handler(dat_work_resourse_page.filter(action=['next', 'prev']))
async def inline_kb_update_works_page_list(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        callback_data_time = callback_data["date"]
        callback_data_time = datetime.strptime(callback_data_time,'%Y-%m-%d %H;%M;%S')
        if (datetime.now() - callback_data_time).total_seconds() < 3600:
            pool: Connection = db
            if callback_data["action"] == 'next':
                arg = int(callback_data["res"]), int(callback_data["page"])*5
            elif callback_data["action"] == 'prev':
                arg = int(callback_data["res"]), int(callback_data["page"])*5-5
            all_works: Record = await pool.fetch("SELECT * from test.public.contract where race_res=$1 limit 5 offset $2", *arg)
            if all_works:
                anws = f'Доступно контрактов - {await pool.fetchval("SELECT count(id) from test.public.contract where race_res=$1", int(callback_data["action"]),)}\n\n'
                list_works = []
                find_user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', int(callback_data["id"]),)
                for item in all_works:
                    work_time_dict = {1: 15, 2: 9, 3: 4, 4: 2, 5: 1}
                    if int(callback_data["res"]) == 1:
                        work_time = work_time_dict[find_user["lvl_prof_bel"]]*item["amount"]
                    elif int(callback_data["res"]) == 2:
                        work_time = work_time_dict[find_user["lvl_prof_cor"]]*item["amount"]
                    elif int(callback_data["res"]) == 3:
                        work_time = work_time_dict[find_user["lvl_prof_acr"]]*item["amount"]
                    list_works.append(emojize(f'[{item["user_guild"]}]<a href="tg://user?id={item["user_id"]}">{item["user_nickname"]}</a>\n'
                                              f'⛓ Количество: {item["amount"]}ед.\n'
                                              f'🕑 Время работы: {work_time}ч.\n'
                                              f'🏵 Стоимость за 1: {item["price"]:,.{0}f} ({item["price"]*item["amount"]:,.{0}f})\n'
                                              f'✅ Принять контракт - <a href="http://t.me/share/url?url={item["link"]}">{item["link"]}</a>\n'.replace(',', ' ')))
                if callback_data["action"] == 'next':
                    await query.bot.edit_message_text(text=anws+'\n'.join(list_works),
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_work_resource_page(callback_data["id"],callback_data_time,int(callback_data["page"])+1,int(callback_data["res"])))
                elif callback_data["action"] == 'prev':
                    await query.bot.edit_message_text(text=anws+'\n'.join(list_works),
                                                      chat_id=query.message.chat.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=await create_cb_work_resource_page(callback_data["id"],callback_data_time,int(callback_data["page"])-1,int(callback_data["res"])))

            else:
                await query.bot.edit_message_text(text='Извини, но тут нет доступных контрактов на данный момент!',
                                                  chat_id=query.message.chat.id,
                                                  message_id=query.message.message_id,
                                                  reply_markup=await create_cb_work_resource_page(callback_data["id"],callback_data_time,1,int(callback_data["res"])))
            await query.answer(cache_time=2)
        else:
            await query.answer(emojize(':cross_mark:Прошло больше часа!!'), cache_time=5)
            await query.message.edit_text('Извини, но данные кнопочки устарели\n'
                                          'используй /find_contract для получения новых')
    else:
        await query.answer(emojize(':cross_mark:Это не твои кнопочки!!'), cache_time=5)